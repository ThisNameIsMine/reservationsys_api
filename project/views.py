import datetime
from .models import Payment, Review, Lesson, Reservation, Notification, UserNew, PromoCode
from .serializers import LessonSerializer, NotificationSerializer, PaymentSerializer, ReviewSerializer, UserBacisSerializer, UserNewSerializer, PromoCodeSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
import secrets
from django.utils import timezone


@api_view(['POST'])
def registerUser(request):    
    serializer = UserNewSerializer(data=request.data)     

    if serializer.is_valid():
        # Serializer will hash the password and create the user if the data is valid
        serializer.save()
        return Response({'status':'success','message': 'User registered successfully','user':serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({'status':'failed','message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def loginUser(request):
    data = request.data
    
    # Retrieve the user based on the provided email
    # return User.objects.get(email=data['email'])
    try:
        # Retrieve the user based on the provided email
        user = UserNew.objects.get(email=data['email'])
        serializer = UserBacisSerializer(user, many=False)

        
        # Check the provided password against the hashed password in the database
        if data['password'] == user.password: #check_password(data['password'], user.password):
            #change return to format {id,name,last_name,email,role,credit}
            
            return Response({'status':'success','message': 'Login successful', 'user': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status':'fail','message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

    except UserNew.DoesNotExist:
        return Response({
            'status':'no_account',
            'message': 'User not found',
            'user': ''
            }, status=status.HTTP_200_OK)  

@api_view(['GET'])
def getAllUsers(request):
    users = UserNew.objects.all()
    serializer = UserNewSerializer(users, many=True)
    #return Response(serializer.data)
    return Response({'status':'success','message':'Users retrieved','data':serializer.data})

@api_view(['GET'])
def getTeachers(request):
    teachers = UserNew.objects.all().filter(role='teacher')
    serializer = UserBacisSerializer(teachers, many=True)
    return Response({'status':'success','message':'Teachers retrieved','data':serializer.data})

@api_view(['GET'])
def getStudents(request):
    students = UserNew.objects.all().filter(role='student')
    serializer = UserBacisSerializer(students, many=True)
    return Response({'status':'success','message':'Students retrieved','data':serializer.data})


# Bude vizadovat miesto student_id precitat s requestu o koho ide, resp. asi bude daco s tokenom    
# Taktiez spravit ako jednu funkciu s teacherom

@api_view(['POST'])
def createNotification(request,id,format=None): # TODO handle sending notifications to multiple users
    try:
        # Retrieve the user based on the provided id
        user = get_object_or_404(UserNew,pk=id)#UserNew.objects.get(id=id)

        # Create a notification for the user
        notification_data = {
            'user': user.id,
            'message_type': 'YourMessageType',  # Provide an appropriate message type
            'message_content': 'Your message content',  # Provide the content of the notification
        }

        serializer = NotificationSerializer(data=notification_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','message':'Notification has been created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except UserNew.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getNotifications(request,id:int,forma=None): 
    # Get the Student instance
    usr = get_object_or_404(UserNew,pk=id)
    # Get notifications associated with the student
    notifications = Notification.objects.filter(user=usr)
    # Serialize the notifications
    serializer = NotificationSerializer(notifications, many=True)

    return Response({'status':'success','message':'Notifications retrieved','data':serializer.data})

@api_view(['GET'])
def getAllNotifications(request):
    notifications = Notification.objects.all()
    serializer = NotificationSerializer(notifications, many=True)
    return Response({'status':'success','message':'All notifications retrieved','data':serializer.data})

#============================== TESTED HANDLE CREATION OF LESSON==================================

@api_view(['POST'])
def createLesson(request,id:int,format=None):
    teacher = get_object_or_404(UserNew,pk=id)
    print(teacher.id)
    print(teacher)


    if teacher.role != 'teacher':
        return Response({'status':'failed','message':'Only teachers can create lessons'})
    else:
        lesson_data = {
            'teacher': teacher.pk,
            'start_time': request.data['start_time'],
            'end_time': request.data['end_time'],            
            'total_slots': request.data['total_slots'],
            'language': request.data['language'],
            'price': request.data['price'],
            'note': request.data['note'],
        }
        print(lesson_data)
        Lesson(teacher=teacher, start_time=request.data['start_time'], end_time=request.data['end_time'], total_slots=request.data['total_slots'], language=request.data['language'], price=request.data['price'], note=request.data['note']).save()
        serializer = LessonSerializer(data=lesson_data, many=False)
        if serializer.is_valid():            
            return Response({'status':'success','message':'Lesson created','data':serializer.data})
        else:
            return Response({'status':'failed','message':'Lesson not created','data':serializer.errors})

    #lesson = Lesson.objects.create(teacher=teacher, start_time=request.data['start_time'], end_time=request.data['end_time'], taken_slots=request.data['taken_slots'], total_slots=request.data['total_slots'], language=request.data['language'], price=request.data['price'], note=request.data['note'])  

@api_view(['GET'])
def getAllLessons(request):
    lessons = Lesson.objects.all()
    serializer = LessonSerializer(lessons, many=True)
    return Response({'status':'success','message':'All lessons retrieved','data':serializer.data})

@api_view(['GET'])
def getLessons(request,id:int,format=None):
    user = get_object_or_404(UserNew,pk=id)
    if user.role == 'teacher':          
        print('reached')  
        lessons = Lesson.objects.filter(teacher=user)        
    elif user.role == 'student':        
        allLesons = Lesson.objects.all()
        lessons =[]
        for lesson in allLesons:
            if lesson.list_of_students.filter(pk=user.id).exists():
                lessons.append(lesson)
            
        #lessons = Lesson.objects.filter(student=user)
    print(lessons)
    serializer = LessonSerializer(lessons, many=True)
    print(serializer)
    print('Data:')
    print(serializer.data)
    for lesson in lessons:
        print(type(serializer))
        #lesson.teacher = UserBacisSerializer(lesson.teacher, many=False).data
    
    return Response({'status':'success','message':'Lessons retrieved','data':serializer.data})

# ============================= TESTED - Join lesson ==========================================
@api_view(['POST'])
def joinLesson(request,format=None):#,id:int
    student = get_object_or_404(UserNew,pk=request.data['student_id'])
    lesson = get_object_or_404(Lesson,pk=request.data['lesson_id'])
    print('student: ',student.id,'lesson: ',lesson.id)
    print(student.role)
    if student.role != 'student':
        return Response({'status':'failed','message':'Only students can join lessons'},status=200)

    if lesson.list_of_students.filter(pk=student.id).exists():
        return Response({'status':'failed','message': 'You are already attending this lesson'}, status=200)
    else:
        if lesson.taken_slots == lesson.total_slots:
            return Response({'status':'failed','message':'Lesson is full'},status=200)
        else:            
            lesson.taken_slots += 1
            reservation = Reservation.objects.create(student=student, lesson=lesson)
            reservation.save()
            lesson.save()
            student.balance -= lesson.price
            student.save()
                
            serializer = LessonSerializer(lesson, many=False)
            return Response({'status':'success','message':'Lesson joined','data':serializer.data},status=200)                

# ============================= TESTED - Leave lesson ==========================================
@api_view(['POST'])
def leaveLesson(request,format=None):#,id:int
    student = get_object_or_404(UserNew,pk=request.data['student_id'])
    lesson = get_object_or_404(Lesson,pk=request.data['lesson_id'])
    print('student: ',student.id,'lesson: ',lesson.id)
    if student.role != 'student':
        return Response({'status':'failed','message':'Only students can leave lessons'},status=200)

    if lesson.list_of_students.filter(pk=student.id).exists():
        if lesson.start_time < timezone.now() + timezone.timedelta(days=1):
            return Response({'status':'failed','message':'You can not leave lesson less than 24h before it starts'},status=200)
        else:
            lesson.taken_slots -= 1        
            lesson.save()
            student.balance += lesson.price
            student.save()
            reservation = Reservation.objects.filter(student=student, lesson=lesson)
            reservation.delete()
            return Response({'status':'success','message':'Lesson left'},status=200)

@api_view(['GET'])
def getLanguages(request):
    # Retrieve the choices from the model
    language_choices = Lesson._meta.get_field('language').choices

    # Convert choices to a list
    languages = [value for key, value in language_choices]
    return Response({'status':'success','message':'Languages retrieved','data':languages})

# =========================== Payments Work in progress ==============================================

@api_view(['POST'])
def createPayment(request,id:int,format=None):
    student = get_object_or_404(UserNew,pk=id)
    teacher = get_object_or_404(UserNew,pk=request.data['teacher'])
    payment = Payment.objects.create(student=student, teacher=teacher, amount=request.data['amount'])
    serializer = PaymentSerializer(payment, many=False) 
    return Response({'status':'success','message':'Payment created','data':serializer.data})

@api_view(['GET'])
def getAllPayments(request):
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response({'status':'success','message':'Payments retrieved','data':serializer.data} )

@api_view(['GET'])
def getUserPayments(request,id:int,format=None):
    user = get_object_or_404(UserNew,pk=id)
    if user.role == 'teacher':
        payments = Payment.objects.filter(teacher=user)
    elif user.role == 'student':
        payments = Payment.objects.filter(student=user)

    serializer = PaymentSerializer(payments, many=True)
    return Response({'status':'success','message':'Payments retrieved','data':serializer.data})

# ============================= Reviews - Work in progress  ============================================
@api_view(['GET'])
def getAllReviews(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response({'status':'success','message':'All reviews retrieved','data':serializer.data})

@api_view(['GET'])
def getReviews(request,id:int,format=None):
    teacher = get_object_or_404(UserNew,pk=id)
    reviews = Review.objects.filter(teacher=teacher.user)
    serializer = ReviewSerializer(reviews, many=True)
    return Response({'status':'success','message':'Reviews retrieved','data':serializer.data})

@api_view(['POST'])
def createReview(request,id:int,format=None):
    student = get_object_or_404(UserNew,pk=id)
    review = Review.objects.create(student=student, teacher=request.data['teacher'], rating=request.data['rating'], review_content=request.data['review_content'])
    serializer = ReviewSerializer(review, many=False)
    return Response({'status':'success','message':'Review created','data':serializer.data})

# ============================= Promocodes - TESTED  ============================================

#promocodes
@api_view(['POST'])
def generatePromoCode(request,format=None):    
    amount = request.data['amount']
    length = 16
    code =  secrets.token_hex(length//2)[:length]
    promocode = PromoCode.objects.create(amount=amount, code=code)
    serializer = PromoCodeSerializer(promocode, many=False)
    return Response({'status':'success','message':'PromoCode created','data':serializer.data})

@api_view(['GET'])
def getAllPromoCodes(request):
    promocodes = PromoCode.objects.all()
    serializer = PromoCodeSerializer(promocodes, many=True)
    return Response({'status':'success','message':'All PromoCodes retrieved','data':serializer.data})

@api_view(['POST'])
def applyPromoCodeToUser(request,id:int,format=None):        
    user = get_object_or_404(UserNew,pk=id)                  
    promocode = get_object_or_404(PromoCode,code=request.data['code'])
    if promocode.used:
        return Response({'status':'failed','message':'PromoCode already used'})
    else:
        user.balance += promocode.amount
        user.save()
        promocode.used = True
        promocode.save()
        return Response({'status':'success','message':'PromoCode used'})



from .models import Payment, Review, Teacher, Student, Lesson, Reservation, Notification, UserNew
from .serializers import NotificationSerializer, PaymentSerializer, ReviewSerializer, TeacherSerializer, UserNewSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password



@api_view(['GET'])
def teacher_list(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response({'Teachers:':serializer.data}, safe=False)


@api_view(['POST'])
def registerUser(request): #TODO
    # data = request.data

    # user = UserNew.objects.create(
    #     firstName = data['firstName'],
    #     lastName = data['lastName'],
    #     email = data['email'],
    #     password = data['password'],
    #     role = data['role']
    # )
    # serializer = UserSerializer(user, many=False)

    # return Response(serializer.data, safe=False)

    serializer = UserNewSerializer(data=request.data)
    
    

    if serializer.is_valid():
        # Serializer will hash the password and create the user if the data is valid
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def loginUser(request):
    data = request.data
    
    # Retrieve the user based on the provided email
    # return User.objects.get(email=data['email'])
    try:
        # Retrieve the user based on the provided email
        user = UserNew.objects.get(email=data['email'])
        serializer = UserNewSerializer(user, many=False)

        
        # Check the provided password against the hashed password in the database
        if data['password'] == user.password: #check_password(data['password'], user.password):
            #change return to format {id,name,last_name,email,role,credit}
            
            return Response({'message': 'Login successful', 'user': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

    except UserNew.DoesNotExist:
        return Response({
            'status':'no_account',
            'message': 'User not found',
            'user': ''
            }, status=status.HTTP_404_NOT_FOUND)  



@api_view(['GET'])
def getTeacherNotifications(request, id:int, format=None):
    # Get the Teacher instance
    teacher = get_object_or_404(Teacher,pk=id) #Teacher.objects.get(id=id)
    # Get notifications associated with the teacher
    notifications = Notification.objects.filter(user=teacher.user)
    # Serialize the notifications
    serializer = NotificationSerializer(notifications, many=True)
    
    return Response(serializer.data, safe=False)


# Bude vizadovat miesto student_id precitat s requestu o koho ide, resp. asi bude daco s tokenom    
# Taktiez spravit ako jednu funkciu s teacherom
@api_view(['GET'])
def getStudentNotifications(request,id:int,forma=None): 
    # Get the Student instance
    student = get_object_or_404(Student,pk=id)
    # Get notifications associated with the student
    notifications = Notification.objects.filter(user=student.user)
    # Serialize the notifications
    serializer = NotificationSerializer(notifications, many=True)
    serializer.save()

    return Response(serializer.data, safe=False)

@api_view(['POST'])
def createNotification(request,id,format=None):
    # Get the user instance
    user = get_object_or_404(UserNew,pk=id)
    # Create the notification
    notification = Notification.objects.create(user=user, message_type=request.data['message_type'], message_content=request.data['message_content'])
    # Serialize the notification
    serializer = NotificationSerializer(notification, many=False)
    serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getAllUsers(request):
    users = UserNew.objects.all()
    serializer = UserNewSerializer(users, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def getAllPayments(request):
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMyPayments(request,id:int,format=None):
    student = get_object_or_404(Student,pk=id)
    payments = Payment.objects.filter(student=student)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createPayment(request,id:int,format=None):
    student = get_object_or_404(Student,pk=id)
    payment = Payment.objects.create(student=student, teacher=request.data['teacher'], amount=request.data['amount'])
    serializer = PaymentSerializer(payment, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getAllReviews(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getReviews(request,id:int,format=None):
    teacher = get_object_or_404(Teacher,pk=id)
    reviews = Review.objects.filter(teacher=teacher.user)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createReview(request,id:int,format=None):
    student = get_object_or_404(Student,pk=id)
    review = Review.objects.create(student=student, teacher=request.data['teacher'], rating=request.data['rating'], review_content=request.data['review_content'])
    serializer = ReviewSerializer(review, many=False)
    return Response(serializer.data)


#vytvaranie hodin
# teacher, start_time, end_time, taken_slots, total_slots, language, price, note, list_of_students

#mazanie hodin ak viac ako 24h pred hodinou




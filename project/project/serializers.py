from rest_framework import serializers
from .models import Payment, Review, Teacher, Student, Lesson, Reservation, Notification, UserNew
#from rest_framework import make_password
from django.contrib.auth.hashers import make_password



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['teacher', 'start_time', 'end_time', 'taken_slots', 'total_slots', 'language', 'price', 'note', 'list_of_students']
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['timestamp', 'message_content','message_type','user'] #'__all__'


class UserNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNew
        fields = ['id', 'firstName', 'lastName', 'email', 'role','password','balance','last_active']


        

        #extra_kwargs = {'password': {'write_only': True}}  # To exclude the password field from the output

    # def create(self, validated_data):
    #     # Hash the password before creating the user
    #     validated_data['password'] = make_password(str(validated_data['password']))
    #     print('#############################################')
    #     print(validated_data)
    #     print(type(validated_data))
    #     print('#############################################')
    #     #raise serializers.ValidationError(validated_data['password'])
    #     user = super(UserNewSerializer, self).create(validated_data)
    #     return user

class UserBacisSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNew
        fields = ['id', 'firstName', 'lastName', 'email', 'role','balance']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
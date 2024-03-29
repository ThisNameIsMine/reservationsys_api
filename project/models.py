from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class UserNew(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)   
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)    
    
    ROLES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=255, choices=ROLES, default='student')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    

    last_active = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firstName + " " + self.lastName + "  " + self.email + " " + self.role


#===================================================================================================

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

# teacher, start_time, end_time, taken_slots, total_slots, language, price, note, list_of_students
class Lesson(models.Model):
    languages = [
        ('english', 'English'),
        ('german', 'German'),
        ('french', 'French'),
        ('spanish', 'Spanish'),
        ('italian', 'Italian'),
        ('russian', 'Russian'),
        ('chinese', 'Chinese'),
        ('japanese', 'Japanese'),
        ('korean', 'Korean'),
        ('arabic', 'Arabic'),
        ('slovak', 'Slovak'),
    ]
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(UserNew, on_delete=models.CASCADE,related_name='lessons_taught')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    taken_slots = models.IntegerField(default=0)
    total_slots = models.IntegerField(default=1)
    language = models.CharField(choices=languages, max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    note = models.TextField(default="")
    list_of_students = models.ManyToManyField(UserNew, through='Reservation',related_name='lessons_attended')
    name = models.CharField(max_length=255, default="")

    

class Reservation(models.Model):
    student = models.ForeignKey(UserNew, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now_add=True)



class Notification(models.Model):
    user = models.ForeignKey(UserNew, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=255)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(UserNew, related_name='payments_as_student', on_delete=models.CASCADE)
    teacher = models.ForeignKey(UserNew, related_name='payments_as_teacher', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    #Add lesson id


class Review(models.Model):
    student = models.ForeignKey(UserNew, related_name='review_as_student', on_delete=models.CASCADE)
    teacher = models.ForeignKey(UserNew, related_name='review_as_teacher', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# To be implemented
class Message(models.Model):
    sender = models.ForeignKey(UserNew, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(UserNew, on_delete=models.CASCADE, related_name='receiver')
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# promo codes, konkretnemu userovi pridat nejaky amount, vratit response - podarilo sa
class PromoCode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.code} - {self.amount}'
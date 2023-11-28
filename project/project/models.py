from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# change on_delete from Cascade to PROTECT ?
#write a function for all users for registration
class UserNew(models.Model):
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

#================================= Don't use these==================================================
class Teacher(models.Model):
    user = models.OneToOneField(UserNew, on_delete=models.CASCADE)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_active = models.DateTimeField(auto_created=True, blank=False)

    def __str__(self):
        return self.user.firstName + " " + self.user.lastName + " - " #+ self.last_active

class Student(models.Model):
    user = models.OneToOneField(UserNew, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #last_active = models.DateTimeField(auto_created=True, blank=True)
    last_active = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + self.last_active
#===================================================================================================

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

# teacher, start_time, end_time, taken_slots, total_slots, language, price, note, list_of_students
class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    taken_slots = models.IntegerField(default=0)
    total_slots = models.IntegerField(default=1)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    note = models.TextField()
    list_of_students = models.ManyToManyField(Student, through='Reservation')


class Reservation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now_add=True)



class Notification(models.Model):
    user = models.ForeignKey(UserNew, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=255)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    #Add lesson id


class Review(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
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

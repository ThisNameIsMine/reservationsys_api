from django.db import models
from django.contrib.auth.models import User

# change on_delete from Cascade to PROTECT ?
#write a function for all users for registration
class UserNew(models.Model):
    # username = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)   
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    # Add other fields as needed (email, name, etc.)

    def __str__(self):
        return self.firstName + " " + self.lastName + "  " + self.email + " - " + self.role

class Teacher(models.Model):
    user = models.OneToOneField(UserNew, on_delete=models.CASCADE)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_active = models.DateTimeField(auto_created=True, blank=True)

    def __str__(self):
        return self.user.firstName + " " + self.user.lastName + " - " #+ self.last_active

class Student(models.Model):
    user = models.OneToOneField(UserNew, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_active = models.DateTimeField(auto_created=True, blank=True)

    def __str__(self):
        return self.user.username + " - " + self.last_active

class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration = models.DurationField()
    available_slots = models.IntegerField()
    reserved_slots = models.IntegerField(default=0)

class Reservation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(UserNew, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=255)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
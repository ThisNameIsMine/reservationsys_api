from django.db import models

# Create your models here.
class User(models.Model):
    # username = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)   
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    # Add other fields as needed (email, name, etc.)

    def __str__(self):
        return self.email
        
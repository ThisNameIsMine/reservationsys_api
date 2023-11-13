from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        email = data.get('email')    
        password = data.get('password')
        role = data.get('role')


        hashed_password = make_password(password)
        User.objects.create(firstName=firstName, password=hashed_password, lastName=lastName, email=email,role=role)

        return JsonResponse({'message': 'User registered successfully'})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=400)

        if check_password(password, user.password):
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'message': 'Invalid password'}, status=400)


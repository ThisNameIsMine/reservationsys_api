"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import getNotifications, loginUser, registerUser, createNotification, generatePromoCode, applyPromoCodeToUser
from project import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #--- Tested ---
    path('registration', registerUser, name="registration"),
    path('login', loginUser, name="login"),    
    path('list/users/all', views.getAllUsers, name='allUsers'),

    path('list/teachers', views.getTeachers, name='getTeachers'),
    path('list/students', views.getStudents, name='getStudents'),

    path('create/lesson/<int:id>', views.createLesson, name='createLesson'), 
    path('list/lessons/all', views.getAllLessons, name='getLesson'),
    path('list/lessons/<int:id>', views.getLessons, name='getLesson'),

    path('create/notification/<int:id>', views.createNotification, name='createNotification'),
    path('list/notifications/<int:id>', getNotifications, name='getUserNotifications'),    
    path('joinlesson', views.joinLesson, name='joinLesson'),
    
    path('create/PromoCode', views.generatePromoCode, name='createPromoCode'),
    path('list/PromoCode/all', views.getAllPromoCodes, name='allPromoCodes'),
    path('use/PromoCode/<int:id>', views.applyPromoCodeToUser, name='usePromoCode'), 
    
    
    #--- NOT Tested ---            
    #path('', views.getInfo, name='info'),


    path('create/Payment/<int:id>', views.createPayment, name='createPayment'),
    path('list/Payments/all', views.getAllPayments, name='allPayments'),
    path('list/Payments/<int:id>', views.getUserPayments, name='getPayment'),
    
    path('create/Review/<int:id>', views.createReview, name='createReview'),
    path('list/Reviews/all', views.getAllReviews, name='allReviews'),      
    path('list/Reviews/<int:id>', views.getReviews, name='getReview'),

    #TODO rating of teacher/student
    # path('create/Rating/<int:id>', views.createRating, name='createRating'),
    # path('list/Ratings/all', views.getAllRatings, name='allRatings'),
    # path('list/Ratings/<int:id>', views.getRatings, name='getRating'),


]

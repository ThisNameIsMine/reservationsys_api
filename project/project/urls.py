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
from .views import getNotifications, loginUser, registerUser, createNotification
from project import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #--- Tested ---
    path('registration/', registerUser, name="registration"),
    path('login/', loginUser, name="login"),
    path('notifications/<int:id>', getNotifications, name='getUserNotifications'),    
    path('crtnotify/<int:id>', views.createNotification, name='createNotification'),
    path('allUsers/', views.getAllUsers, name='allUsers'),
    #--- NOT Tested ---
    path('allPayments/', views.getAllPayments, name='allPayments'),
    path('allReviews/', views.getAllReviews, name='allReviews'),
    path('crtPayment/<int:id>', views.createPayment, name='createPayment'),
    path('crtReview/<int:id>', views.createReview, name='createReview'),
    path('getReviews/<int:id>', views.getReviews, name='getReview'),


]

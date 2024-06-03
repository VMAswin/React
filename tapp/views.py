# users/views.py
from rest_framework import viewsets
from .models import Customuser,UserProfile
from rest_framework import generics,status
from .serializers import UserSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
import string
import random
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = Customuser.objects.all()
#     serializer_class = UserSerializer

#     def perform_create(self, serializer):
#         user = serializer.save()
#         random_password = ''.join(random.choices(string.digits, k=6))
#         user.set_password(random_password)
#         user.save()
#         send_mail(
#             'Welcome!',
#             'Thank you for registering.'+random_password,
#             settings.EMAIL_HOST_USER,
#             [user.email],
#             fail_silently=False,
#         )

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    # password = request.data.get('password')
    user_type = request.data.get('user_type')
    # Create User object and save to database
    password = ''.join(random.choices(string.digits, k=6))
    user = Customuser.objects.create(username=username, email=email,user_type=user_type)
    user.set_password(password)
    user.save()
    phone_number = request.data.get('phone_number')
    certificate = request.data.get('certificate')
    department = request.data.get('department')
    image = request.data.get('profile')
    usr = UserProfile.objects.create(user=user,phone_number=phone_number,department=department,Image=image,certificate=certificate)
    usr.save()
    subject='Regsitration Success'
    message='username:'+str(username)+"\n"+'password:'+str(password)+"\n"+'email:'+str(email)
    send_mail(subject,message,settings.EMAIL_HOST_USER,{user.email})
    messages.info(request,'Registration success, please check your email for username and password..')
    return Response({'message': 'User registered successfully'})

class Trainers(APIView):
    def view(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            trainers = Customuser.objects.filter(user_type=2)
            refresh = RefreshToken.for_user(trainers)
            return JsonResponse({'access':str(refresh.access_token),'trainers':trainers},safe=False)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(username = email, password = password)
            print('hai')
            print(user)
            if user:
                refresh = RefreshToken.for_user(user)
                
                print(refresh.access_token)
                return JsonResponse({'access':str(refresh.access_token)},safe=False)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# users/views.py
from rest_framework import viewsets
from .models import Customuser,UserProfile,Department,Trainer
from rest_framework import generics,status
from .serializers import UserSerializer,LoginSerializer,TrainerSerializer
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
from django.db.models import Q
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

class TrainersViewSet(viewsets.ModelViewSet):
    queryset = Customuser.objects.filter(~Q(user_type=0)).filter(~Q(user_type=1))
    serializer_class = UserSerializer

@api_view(['POST'])
def add_dept(request):
    deptname = request.data.get('Department_name')
    descript = request.data.get('Description')
    dept = Department.objects.create(Department_name=deptname,Description=descript)
    dept.save()
    return Response({'message': 'Department Successfully added'})

@api_view(['POST'])
def add_tr_attend(request):
    trainer = request.data.get('Trainer_name')
    date = request.data.get('Date')
    status = request.data.get('status')
    tr = Trainer.objects.create(Trainer_name=trainer,Date=date,status=status)
    tr.save()
    return Response({'message': 'Attendence Successfully added'})
class TrainerAttendenceViewSet(viewsets.ModelViewSet):
    queryset= Trainer.objects.all()
    serializer_class = TrainerSerializer

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
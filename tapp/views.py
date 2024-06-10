# users/views.py
from rest_framework import viewsets
from .models import Customuser,UserProfile,Department,Trainer,Projects,Trainee,Leave,Uploadprojects,Allocation
from rest_framework import generics,status
from .serializers import UserSerializer,LoginSerializer,TrainerSerializer,DepartmentSerializer,TraineeSerializer,ProjectSerializer,LeaveSerializer,USerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
import string
import random
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import auth
from django.contrib.auth.models import update_last_login


@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
   
    user_type = request.data.get('user_type')
    
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


def allocate_t(request):
    queryset = Customuser.objects.filter(user_type=3)
    data = list(queryset.values('id', 'username'))  
    return JsonResponse(data, safe=False)

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

@api_view(['POST'])
def allocate(request):
    trainer = request.data.get('trainer_name')
    trainee = request.data.get('trainee_name')
    t = Allocation.objects.create(trainer_name=trainer,trainee_name=trainee)
    t.save()
    return Response({'message': 'Allocated'})
class TrainerAttendenceViewSet(viewsets.ModelViewSet):
    queryset= Trainer.objects.all()
    serializer_class = TrainerSerializer

@api_view(['POST'])
def allocate_projects(request):
    proj_name = request.data.get('project_name')
    std = request.data.get('start_date')
    end = request.data.get('end_date')
    pro = Projects.objects.create(project_name=proj_name,start_date=std,end_date=end)
    pro.save()
    return Response({'message': 'Project Successfully alloted'})

@api_view(['POST'])
def add_trainee_attend(request):
    trainee = request.data.get('Trainee_name')
    date = request.data.get('Date')
    status = request.data.get('status')
    tr = Trainee.objects.create(Trainee_name=trainee,Date=date,status=status)
    tr.save()
    return Response({'message': 'Attendence Successfully added'})

class TraineeAttendenceViewSet(viewsets.ModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

@api_view(['POST'])
def apply_leave_tr(request):
    name = request.data.get('name')
    role = request.data.get('role')
    std = request.data.get('start_date')
    end = request.data.get('end_date')
    pro = Leave.objects.create(name=name,start_date=std,end_date=end,role=role)
    pro.save()
    return Response({'message': 'Leave Applied'})



    
@api_view(['POST'])
def trm_reset(request):
    username = request.data.get('username')
    old_password = request.data.get('Current_password')
    new_password = request.data.get('New_password')

    user = authenticate(username=username, password=old_password)
    if user is not None:
        if len(new_password) < 6 or not any(char.isupper() for char in new_password) \
                     or not any(char.isdigit() for char in new_password) \
                     or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in new_password):
                     messages.error(request, 'Password must be at least 6 characters long and contain at least one uppercase letter, one digit, and one special character, or entered password does not match')
                     r=0
                     return JsonResponse({'message': 'Password Must meet the criteria','r':r})
        else:
            user.set_password(new_password)
            user.save()
            r=1
            return Response({"message": "Password reset successful",'r':r}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def tr_reset(request):
    username = request.data.get('username')
    old_password = request.data.get('Current_password')
    new_password = request.data.get('New_password')

    user = authenticate(username=username, password=old_password)
    if user is not None:
        if len(new_password) < 6 or not any(char.isupper() for char in new_password) \
                     or not any(char.isdigit() for char in new_password) \
                     or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in new_password):
                     messages.error(request, 'Password must be at least 6 characters long and contain at least one uppercase letter, one digit, and one special character, or entered password does not match')
                     r=0
                     return JsonResponse({'message': 'Password Must meet the criteria','r':r})
        else:
            user.set_password(new_password)
            user.save()
            r=1
            return Response({"message": "Password reset successful",'r':r}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def t_reset(request):
    username = request.data.get('username')
    old_password = request.data.get('Current_password')
    new_password = request.data.get('New_password')

    user = authenticate(username=username, password=old_password)
    if user is not None:
        if len(new_password) < 6 or not any(char.isupper() for char in new_password) \
                     or not any(char.isdigit() for char in new_password) \
                     or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in new_password):
                     messages.error(request, 'Password must be at least 6 characters long and contain at least one uppercase letter, one digit, and one special character, or entered password does not match')
                     r=0
                     return JsonResponse({'message': 'Password Must meet the criteria','r':r})
        else:
            user.set_password(new_password)
            user.save()
            r=1
            return Response({"message": "Password reset successful",'r':r}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['POST'])
def upload_projects(request):
    proj = request.data.get('project_name')
    date = request.data.get('date')
    file = request.data.get('file')
    pro = Uploadprojects.objects.create(project_name=proj,date=date,file=file)
    pro.save()
    return Response({'message': 'Uploaded'})

@api_view(['POST'])
def apply_leave_t(request):
    name = request.data.get('name')
    role = request.data.get('role')
    std = request.data.get('start_date')
    end = request.data.get('end_date')
    pro = Leave.objects.create(name=name,start_date=std,end_date=end,role=role)
    pro.save()
    return Response({'message': 'Leave Applied'})






                
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        user_type=user.user_type
        if user_type == 0:
            role = 'Admin'
        elif user_type == 1:
           role = 'Trainee Manager'
        elif user_type == 2:
            role = 'Trainer'
        else:
            role = 'Trainee'
        update_last_login(None, user)
        return JsonResponse({"message": "Login successful",'role':role}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


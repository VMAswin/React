# users/views.py
from rest_framework import viewsets
from .models import Customuser,UserProfile,Department,Trainer,Projects,Trainee,Leave,Uploadprojects
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


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def trm_reset(request):
    current = request.data.get('Current_password')
    new = request.data.get('New_password')
    confirm = request.data.get('confirm_password')
    # user = USerializer(request.user)
    user = request.user.id
    print(user)
    print('hai')
    tr = Customuser.objects.get(id=user)
    curpas = tr.password
    checkpass = check_password(current,curpas)
    if checkpass:
        if new == confirm:
            if len(new) < 6 or not any(char.isupper() for char in new) \
                    or not any(char.isdigit() for char in new) \
                    or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in new):
                    messages.error(request, 'Password must be at least 6 characters long and contain at least one uppercase letter, one digit, and one special character, or entered password does not match')
                    return Response({'message': 'Password Must meet the criteria'})
            else:
                
                    usr = request.user.id
                    tsr=Customuser.objects.get(id=usr)
                    tsr.password=new
                    tsr.set_password(new)
                    tsr.save()
                    return Response({'message': 'Password Reset'})
    else:
        return Response({'message': 'Password not'})


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





class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(username = email, password = password)
            if user:
                user_type=user.user_type
                if user_type == 0:
                    role = 'Admin'
                elif user_type == 1:
                    role = 'Trainee Manager'
                elif user_type == 2:
                    role = 'Trainer'
                else:
                    role = 'Trainee'
                refresh = RefreshToken.for_user(user)
                
                print(refresh.access_token)
                return JsonResponse({'access':str(refresh.access_token),'role':role},safe=False)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                


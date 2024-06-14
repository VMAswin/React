# users/views.py
from rest_framework import viewsets
from .models import Customuser,UserProfile,Department,Trainer,Projects,Trainee,Leave,Uploadprojects,Allocation,Notifications,Schedule
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
from django.views import View
from django.views.decorators.http import require_GET
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


@csrf_exempt
@api_view(['POST'])
def add_trainer(request):
    data = json.loads(request.body)
    dep_name = data.get('selectedValue')
    trainer_name = data.get('trainer_name')
    email = data.get('email')
    phone = data.get('phone_number')
    certificate = data.get('certificate')
    image = request.data.get('profile')
    dep = Department.objects.get(id=dep_name)
    department_name=dep.Department_name
    password = ''.join(random.choices(string.digits, k=6))
    trainer = Customuser.objects.create(username=trainer_name,email=email,user_type=2,is_approved=1)
    trainer.set_password(password)
    trainer.save()
    usr = UserProfile.objects.create(user=trainer,phone_number=phone,department=department_name,Image=image,certificate=certificate)
    usr.save()   
    subject='Your Profile has been added'
    message='username:'+str(trainer_name)+"\n"+'password:'+str(password)+"\n"+'email:'+str(email)
    send_mail(subject,message,settings.EMAIL_HOST_USER,{trainer.email})
    messages.info(request,'Registration success, please check your email for username and password..')
    return Response({'message': 'User registered successfully'})



@api_view(['POST'])
def add_dept(request):
    deptname = request.data.get('Department_name')
    descript = request.data.get('Description')
    dept = Department.objects.create(Department_name=deptname,Description=descript)
    dept.save()
    return Response({'message': 'Department Successfully added'})




class TrainerAttendenceViewSet(viewsets.ModelViewSet):
    queryset= Trainer.objects.all()
    serializer_class = TrainerSerializer







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
    us = Customuser.objects.get(username=username)
    if us.is_approved == 1 and us.user_type == 3:
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
            refresh = RefreshToken.for_user(user)
            return JsonResponse({"message": "Login successful",'role':role,'user_type':user_type,'access':str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    elif us.user_type == 1 or us.user_type == 2:
        user = authenticate(username=username, password=password)
        if user is not None:
            user_type=user.user_type
            if user_type == 0:
                role = 'Admin'
            elif user_type == 1:
                role = 'Trainee Manager'
            elif user_type == 2:
                role = 'Trainer'
            update_last_login(None, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({"message": "Login successful",'role':role,'user_type':user_type,'access':str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return JsonResponse({"message": "Approval Pending"}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def approve(request,id):
    try:
         user = Customuser.objects.get(id=id)
         user.is_approved = 1
         user.save()
         return Response({'status': 'User approved'}, status=status.HTTP_200_OK)
    except Customuser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def approve_leave(request,id):
    try:
         user = Leave.objects.get(id=id)
         user.is_approved = 1
         user.save()
         return Response({'status': 'Leave approved'}, status=status.HTTP_200_OK)
    except Customuser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def reject_leave(request,id):
    try:
         user = Leave.objects.get(id=id)
         user.is_approved = 2
         user.save()
         return Response({'status': 'Leave not approved'}, status=status.HTTP_200_OK)
    except Customuser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@require_GET
def trainers(request):
     trainers = Customuser.objects.filter(user_type=2)
     data = list(trainers.values('id','username','email'))
     return JsonResponse(data,safe=False)

@require_GET
def vt_atd_trm(request):
     trainees = Trainee.objects.all()
     data = list(trainees.values('id','Trainee_name','Date','status'))
     return JsonResponse(data,safe=False)

@api_view(['POST'])
def Remove(request,id):
     try:
          user = Customuser.objects.get(id=id)
          user.delete()
          return Response({'message':'User Removed'},status=status.HTTP_200_OK)
     except Customuser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@require_GET
def approve_disapprove(request):
    ad = Customuser.objects.filter(is_approved=0).filter(~Q(user_type=1)).filter(~Q(user_type=0))
    data = list(ad.values('id','username','email','is_approved'))
    return JsonResponse(data,safe=False)

@require_GET
def view_leave(request):
     leaves = Leave.objects.all()
     data = list(leaves.values('id','name','role','start_date','end_date'))
     return JsonResponse(data,safe=False)


@api_view(['POST'])
def add_noti(request):
    notifi = request.data.get('notification')
    no = Notifications.objects.create(Notification=notifi)
    no.save()
    return Response({"message": "Notification sent"})



@require_GET
def add_trainer_attend(request):
     tra = Customuser.objects.filter(user_type=2)
     data = list(tra.values('id','username'))
     return JsonResponse(data,safe=False)



@api_view(['POST'])
def add_tr_attend(request):
    trainer = request.data.get('Trainer_name')
    date = request.data.get('Date')
    status = request.data.get('status')
    tr = Trainer.objects.create(Trainer_name=trainer,Date=date,status=status)
    tr.save()
    return Response({'message': 'Attendence Successfully added'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_GET
def t_attend(request):
    user = request.user
    uid = user.id
    attend = Trainee.objects.filter(trainee_id=uid)
    data = list(attend.values('id','Trainee_name','Date','status'))
    return JsonResponse(data,safe=False)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_GET
def view_allocated_trainees(request):
    user = request.user
    trainee = Allocation.objects.filter(trainer_name=user)
    data = list(trainee.values('id','trainee_name'))
    return JsonResponse(data,safe=False)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_GET
def vt_attend(request):
     user = request.user
     allo = Allocation.objects.get(trainer_name=user)
     trainee = allo.trainee_name
     attend = Trainee.objects.filter(Trainee_name=trainee)
     data = list(attend.values('id','Trainee_name','Date','status'))
     return JsonResponse(data,safe=False)


@require_GET
def add_trainers(request):
     dep = Department.objects.all()
     data = list(dep.values('id','Department_name'))
     return JsonResponse(data,safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_GET
def trainer_attend_TR(request):
    user = request.user
    uid = user.id
    attend = Trainer.objects.filter(trainer_id=uid)
    data = list(attend.values('id','Trainer_name','Date','status'))
    return JsonResponse(data,safe=False)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def allocate_projects(request):
    proj_name = request.data.get('project_name')
    std = request.data.get('start_date')
    end = request.data.get('end_date')
    user = request.user
    uid = user.id
    trainer = Customuser.objects.get(id=uid)
    pro = Projects.objects.create(project_name=proj_name,start_date=std,end_date=end,trainer=trainer)
    pro.save()
    return Response({'message': 'Project Successfully alloted'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_projects(request):
    proj = request.data.get('project_name')
    date = request.data.get('date')
    file = request.data.get('file')
    user = request.user
    uid = user.id
    trainee = Customuser.objects.get(id=uid)
    trainee_name = trainee.username
    pro = Uploadprojects.objects.create(project_name=proj,date=date,file=file,trainee=trainee,trainee_name=trainee_name)
    pro.save()
    return Response({'message': 'Uploaded'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_GET
def view_uploaded_projects_tr(request):
     user = request.user
     traine = Allocation.objects.get(trainer_name=user)
     traine_name = traine.trainee_name
     traine_id = Customuser.objects.get(username=traine_name)
     proj = Uploadprojects.objects.filter(trainee=traine_id)
     data = list(proj.values('id','project_name','date','file','trainee_name'))
     return JsonResponse(data,safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_GET
def view_projects(request):
     user = request.user
     tra = Allocation.objects.get(trainee_name=user)
     tra_name = tra.trainer_name
     tra_id = Customuser.objects.get(username=tra_name)
     pro = Projects.objects.filter(trainer=tra_id)
     data = list(pro.values('id','project_name','start_date','end_date'))
     return JsonResponse(data,safe=False)




@require_GET
def class_schedule_trainers(request):
     trainers = Customuser.objects.filter(user_type=2)
     data = list(trainers.values('id','username'))
     return JsonResponse(data,safe=False)

@csrf_exempt
@api_view(['POST'])
def add_class_schedule(request):
     data = json.loads(request.body)
     tr = data.get('selectedValue')
     date = data.get('Date')
     from_time = data.get('from')
     to_time = data.get('to')
     trainer = Customuser.objects.get(id=tr)
     schedule = Schedule.objects.create(Date=date,From=from_time,To=to_time,Trainer=trainer)
     schedule.save()
     return Response({'message': 'Scheduled'})

@require_GET
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_class_TR(request):
     user = request.user
     uid = user.id
     cs = Schedule.objects.filter(Trainer=uid)
     data = list(cs.values('id','Date','From','To'))
     return JsonResponse(data,safe=False)

@require_GET
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_class_T(request):
     user = request.user
     trai = Allocation.objects.get(trainee_name=user)
     trainer = trai.trainer_name
     tid = Customuser.objects.get(username=trainer)
     cs = Schedule.objects.filter(Trainer=tid)
     data = list(cs.values('id','Date','From','To'))
     return JsonResponse(data,safe=False)



@require_GET
def trainees_alo(request):
     tra = Customuser.objects.filter(user_type=3)
     data = list(tra.values('id','username'))
     return JsonResponse(data,safe=False)

@require_GET
def trainers_alo(request):
     tra = Customuser.objects.filter(user_type=2)
     data = list(tra.values('id','username'))
     return JsonResponse(data,safe=False)

@csrf_exempt
@api_view(['POST'])
def allocate(request):
    data = json.loads(request.body)
    trainer = data.get('selectedTrainer')
    trainee = data.get('selectedValue')
    tr = Customuser.objects.get(id=trainer)
    tr_name = tr.username
    t = Customuser.objects.get(id=trainee)
    t_name = t.username
    dep = UserProfile.objects.get(user_id=trainer)
    dep_name = dep.department
    department = Department.objects.get(Department_name=dep_name)
    allocat = Allocation.objects.create(trainer_name=tr_name,trainee_name=t_name,department=department)
    allocat.save()
    return Response({'message': 'Allocated'})


@require_GET
def trainees(request):
     trainees = Customuser.objects.filter(user_type=3)
     data = list(trainees.values('id','username','email'))
     return JsonResponse(data,safe=False)


@require_GET
def add_trainee_attend(request):
     tra = Customuser.objects.filter(user_type=3)
     data = list(tra.values('id','username'))
     return JsonResponse(data,safe=False)
     

@csrf_exempt
@api_view(['POST'])
def add_trainee_atd(request):
    data = json.loads(request.body)
    name = data.get('selectedValue')
    date = data.get('Date')
    statu = data.get('status')
    tr = Customuser.objects.get(id=name)
    tr_name=tr.username
    trainee = Trainee.objects.create(Trainee_name=tr_name,Date=date,status=statu,trainee=tr)
    trainee.save()   
    return Response({'status': 'success'}, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
def add_trainer_atd(request):
    data = json.loads(request.body)
    name = data.get('selectedValue')
    date = data.get('Date')
    statu = data.get('status')
    tr = Customuser.objects.get(id=name)
    tr_name=tr.username
    trainee = Trainer.objects.create(Trainer_name=tr_name,Date=date,status=statu,trainer=tr)
    trainee.save()   
    return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
    


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainerAttendenceViewSet,TraineeAttendenceViewSet,ProjectViewSet
from .import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
# router.register(r'trainers',TrainersViewSet)
router.register(r'vtr_attend',TrainerAttendenceViewSet)
router.register(r'vt_attend',TraineeAttendenceViewSet)
router.register(r'view_projects',ProjectViewSet)
# router.register(r'view_leave',LeaveViewSet)
# router.register(r'allocate_t',TViewSet,basename='traine')
# router.register(r't_attend',TrainerAttendenceViewSet)





urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login',views.login,name='login'),
    path('users/',views.register_user,name='users'),
    path('add_dept',views.add_dept,name='add_dept'),
    path('add_tr_attend',views.add_tr_attend,name='add_tr_attend'),
    path('allocate_projects',views.allocate_projects,name='allocate_projects'),
    path('add_trainee_attend',views.add_trainee_attend,name='add_trainee_attend'),
    path('apply_leave_tr',views.apply_leave_tr,name='apply_leave_tr'),
    path('trm_reset',views.trm_reset,name='trm_reset'),
    path('tr_reset',views.tr_reset,name='tr_reset'),
    path('t_reset',views.t_reset,name='t_reset'),
    path('upload_projects',views.upload_projects,name='upload_projects'),
    path('apply_leave_t',views.apply_leave_t,name='apply_leave_t'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('allocate',views.allocate,name='allocate'),
    path('approve_disapprove/',views.approve_disapprove,name='approve_disapprove'),
    path('approve/<int:id>',views.approve,name='approve'),
    path('logout',views.logout,name='logout'),
    path('add_noti',views.add_noti,name='add_noti'),
    path('add_trainee_atd',views.add_trainee_atd,name='add_trainee_atd'),
    path('t_attend',views.t_attend,name='t_attend'),
    path('trainees',views.trainees,name='trainees'),
    path('trainers/',views.trainers,name='trainers'),
    path('remove/<int:id>',views.Remove,name='remove'),
    path('add_trainers',views.add_trainers,name='add_trainers'),
    path('add_trainer',views.add_trainer,name='add_trainer'),
    path('vt_atd_trm',views.vt_atd_trm,name='vt_atd_trm'),
    path('view_leave',views.view_leave,name='view_leave'),
    path('approve_leave/<int:id>',views.approve_leave,name='approve_leave'),
    path('reject_leave/<int:id>',views.reject_leave,name='reject_leave'),
    path('add_trainer_attend',views.add_trainer_attend,name='add_trainer_attend'),
    path('add_trainer_atd',views.add_trainer_atd,name='add_trainer_atd'),
    path('trainer_attend_TR',views.trainer_attend_TR,name='trainer_attend_TR'),
    path('trainees_alo',views.trainees_alo,name='trainees_alo'),
    path('trainers_alo',views.trainers_alo,name='trainers_alo'),
    path('view_allocated_trainees',views.view_allocated_trainees,name='view_allocated_trainees'),
    

    
]
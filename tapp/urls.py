from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainersViewSet,TrainerAttendenceViewSet,TraineeAttendenceViewSet,ProjectViewSet,LeaveViewSet
from .import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'trainers',TrainersViewSet)
router.register(r'vtr_attend',TrainerAttendenceViewSet)
router.register(r'vt_attend',TraineeAttendenceViewSet)
router.register(r'view_projects',ProjectViewSet)
router.register(r'view_leave',LeaveViewSet)






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
    path('allocate_t',views.allocate_t,name='allocate_t'),
    path('allocate',views.allocate,name='allocate'),
    path('approve_disapprove/',views.approve_disapprove,name='approve_disapprove'),
    path('logout',views.logout,name='logout'),
    path('add_noti',views.add_noti,name='add_noti')
    

    
]
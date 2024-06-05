from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView,TrainersViewSet,TrainerAttendenceViewSet,TraineeAttendenceViewSet,ProjectViewSet,LeaveViewSet
from .import views

router = DefaultRouter()
router.register(r'trainers',TrainersViewSet)
router.register(r'vtr_attend',TrainerAttendenceViewSet)
router.register(r'vt_attend',TraineeAttendenceViewSet)
router.register(r'view_projects',ProjectViewSet)
router.register(r'view_leave',LeaveViewSet)
# router.register(r't_attend',TrainerAttendenceViewSet)





urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login',LoginView.as_view(),name='login'),
    path('users/',views.register_user,name='users'),
    path('add_dept',views.add_dept,name='add_dept'),
    path('add_tr_attend',views.add_tr_attend,name='add_tr_attend'),
    path('allocate_projects',views.allocate_projects,name='allocate_projects'),
    path('add_trainee_attend',views.add_trainee_attend,name='add_trainee_attend'),
    path('apply_leave_tr',views.apply_leave_tr,name='apply_leave_tr'),
    # path('trm_reset',views.trm_reset,name='trm_reset'),
    path('upload_projects',views.upload_projects,name='upload_projects'),
    path('apply_leave_t',views.apply_leave_t,name='apply_leave_t'),
    # path('api/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    

    
]
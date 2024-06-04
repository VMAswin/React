from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView,TrainersViewSet,TrainerAttendenceViewSet
from .import views
router = DefaultRouter()
router.register(r'trainers',TrainersViewSet)
router.register(r'vtr_attend',TrainerAttendenceViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login',LoginView.as_view(),name='login'),
    path('users/',views.register_user,name='users'),
    path('add_dept',views.add_dept,name='add_dept'),
    path('add_tr_attend',views.add_tr_attend,name='add_tr_attend'),
    # path('trm_reset',views.trm_reset,name='trm_reset'),
    

    
]
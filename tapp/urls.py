from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView,Trainers
from .import views
router = DefaultRouter()
# router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login',LoginView.as_view(),name='login'),
    path('users/',views.register_user,name='users'),
    path('trainers',Trainers.as_view(),name='trainers')
]
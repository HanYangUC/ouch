from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
# from .views import TodoListViewSet, oauthToken, MyCustomSocialSignupForm
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegistrationViewSet, UserViewSet, CustomAuthToken, LoginView, TimeslotViewset

router = DefaultRouter()

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    
    path('register/', RegistrationViewSet.as_view({'post': 'post'}), name='register'),
    path('getall/', UserViewSet.as_view({'get': 'list'}), name='list'),
    # path('authenticate-token/', LoginView.as_view()),
    path('authenticate-token/', CustomAuthToken.as_view()),
    path('add-timeslot/', TimeslotViewset.as_view({'post': 'post'}), name='add_timeslot'),
    path('get-timeslot/<int:id>/', TimeslotViewset.as_view({'get': 'list'}), name='add_timeslot'),
    path('get-timeslot/', TimeslotViewset.as_view({'get': 'list'}), name='get_timeslot'),
    path('get-free-slot/', TimeslotViewset.as_view({'get': 'get_free_slot'}), name='get_freeslot'),
    path('get-free-slot/<int:id>/', TimeslotViewset.as_view({'get': 'get_free_slot'}), name='get_freeslot'),
    
    
    
    
    
    path('update-timeslot/', TimeslotViewset.as_view({'post': 'update_timeslot'}), name='update_timeslot'),
    path('get-timeslotss/<int:id>/', TimeslotViewset.as_view({'get': 'get_timeslotss'}), name='update_timeslot'),
    path('get-timeslotss/', TimeslotViewset.as_view({'get': 'get_timeslotss'}), name='update_timeslot'),
    
]
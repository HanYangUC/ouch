from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
# from .views import TodoListViewSet, oauthToken, MyCustomSocialSignupForm
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegistrationViewSet, UserViewSet, CustomAuthToken, TimeslotViewset

router = DefaultRouter()

urlpatterns = [
    path('register/', RegistrationViewSet.as_view({'post': 'post'}), name='register'),
    path('getall/', UserViewSet.as_view({'get': 'list'}), name='list'),
    path('authenticate-token/', CustomAuthToken.as_view(), name='login'),
    path('update-timeslot/', TimeslotViewset.as_view({'post': 'update_timeslot'}), name='update_timeslot'),
    path('get-timeslots/<int:id>/', TimeslotViewset.as_view({'get': 'get_timeslots'}), name='get_timeslot'),
    path('get-timeslots/', TimeslotViewset.as_view({'get': 'get_timeslots'}), name='get_timeslot'),
    
]
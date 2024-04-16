from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
# from .views import TodoListViewSet, oauthToken, MyCustomSocialSignupForm
from django.views.generic import TemplateView

from .views import RegistrationViewSet, UserViewSet, CustomAuthToken

router = DefaultRouter()

urlpatterns = [
    path('register/', RegistrationViewSet.as_view({'post': 'post'}), name='register'),
    path('getall/', UserViewSet.as_view({'get': 'list'}), name='list'),
    path('authenticate-token/', CustomAuthToken.as_view()),
]
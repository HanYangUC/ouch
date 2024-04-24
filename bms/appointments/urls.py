from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AppointmentViewset
router = DefaultRouter()

urlpatterns = [
    path('create/', AppointmentViewset.as_view({'post':'create'}), name='create_appointment'),
    path('list/', AppointmentViewset.as_view({'get':'list'}), name='create_appointment'),
    path('cancel/<int:id>/', AppointmentViewset.as_view({'put':'cancel'}), name='cancel_appointment'),
]
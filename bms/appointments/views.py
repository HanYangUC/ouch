from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import AppointmentSerializer
# Create your views here.
from accounts.models import User
from appointments.models import Appointment
from .utils import send_email, send_email_cancel

class AppointmentViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (TokenAuthentication, )
    
    def list(self, request, *args, **kwargs):
        queryset = Appointment.objects.all()
        serializer = AppointmentSerializer(queryset, many=True)
        return Response({'Appointment': serializer.data})
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        appointment_exist = Appointment.objects.filter(barber=data.get('barber'), start_time=data.get('start_time'), date=data.get('date')).exists()
        if appointment_exist:
            return Response({'Error': 'Timeslot is booked'})
        
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            return Response({'Success': serializer.data})
        return Response({'Error' : 'Invalid input'})
        
        
    def cancel(self, request, id, *args, **kwargs):
        appointment = Appointment.objects.filter(id=id).first()
        if not appointment:
            return Response({'Error': 'Invalid appointment ID'})
        
        if not (request.user.id == appointment.barber.id or request.user.id == appointment.customer.id):
            return Response({'Error': 'User not associated to appointment'})
        
        if appointment.is_cancelled:
            return Response({'Error': 'Appointment is already cancelled'})
        
        appointment.is_cancelled = True
        appointment.save()
        send_email_cancel(appointment=appointment)
        return Response({'Success': 'Appointment is cancelled'})
        
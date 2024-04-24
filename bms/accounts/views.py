from django.shortcuts import render

# Create your views here.
from . import serializers
from .models import User, BarberTimeslot
from appointments.models import Appointment
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime
from django.db.models import Q
from datetime import datetime
class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RegistrationSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            
        return Response({'Success': 'Successfully registered'})
    

class UserViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = User.objects.get_queryset()
        user_list = serializers.UserSerializer(queryset, many=True)
        return Response(user_list.data)
    

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        # print(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'username': user.username,
        }
        return Response(data)





class TimeslotViewset(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def update_timeslot(self, request, *args, **kwargs):
        data = request.data.copy()
        timeslot = data.get('timeslot')
        day_of_week = data.get('day_of_week')
        barber = request.user
        barber_timeslot, created = BarberTimeslot.objects.get_or_create(
            user=barber,
            day_of_week=day_of_week,
            defaults={'timeslot': timeslot}
        )
        if created:
            return Response({'Success': 'Created timeslot for barber'})
        else:
            appointments = Appointment.objects.filter(
                Q(barber=barber) & 
                Q(date__week_day=(int(day_of_week)+2)%7) & #1=sunday, 7=saturday, my default is 0=monday, 6=sunday, %7 to make 6 = sunday
                Q(date__gte=datetime.now().date())
            )
            if not appointments.exists():
                barber_timeslot.timeslot = timeslot
                barber_timeslot.save()
                
            else:
                active_timeslot = [app.start_time for app in appointments]
                old_timeslot = barber_timeslot.timeslot
                for booked_slot in active_timeslot:
                    if old_timeslot[booked_slot] == '1' and timeslot[booked_slot] == '0':
                        return Response({'Error': 'Active booking, cannot update (or cancel the appointment before updating)'})
                    
                
                
                
                barber_timeslot.timeslot = timeslot
                barber_timeslot.save()
                    
            return Response({'Success': 'Timeslot updated'})
            
    
    def get_timeslots(self, request, id=None, val_date=None, *args, **kwargs):
        from django.db.models import Case, When, Value, IntegerField
        
        if val_date:
            date = val_date
            if date < datetime.today().date():
                raise Response({'Error': 'Cannot be earlier than today'})
        else: 
            date = datetime.strptime(request.GET.get('date'), "%d-%m-%Y") or val_date
            if date.date() < datetime.today().date():
                return Response({'Error': 'Cannot be earlier than today'})
        full_timeslot = []
        
        if not id:
            area = request.GET.get('area', None)
            barber_timeslot = BarberTimeslot.objects.filter(
                Q(day_of_week=date.weekday())
            )
            if area:
                barber_timeslot = barber_timeslot.filter(user__area=area)
            appo = Appointment.objects.filter(
                Q(date=date)
            )
            booked_slot = [(a.barber.id, a.start_time) for a in appo]
            
            full_timeslot ={}
            for barber in barber_timeslot:
                full_timeslot.update({
                    barber.user.id: barber.timeslot
                    })
            time = request.GET.get('time', None)
            for barber, start_time in booked_slot:
                full_timeslot[barber] = full_timeslot[barber][:start_time] + 'x' + full_timeslot[barber][start_time + 1:] # 'x' = taken, 0 = not working, 1 = available
            data = {}
                
            if time is not None:
                time = int(time)
                for barber in barber_timeslot:
                    if full_timeslot[barber.user.id][int(time)] == '1': #the selected slot
                        data.update({
                                barber.user.id : {
                                    "name": barber.user.name, 
                                    "area": barber.user.area
                                }
                            }
                        )
            
                if not data:
                    return Response({'Error': 'No available barber in selected timeslot'})
                else:
                    return Response({f'Available on {time}': data})

            if not len(full_timeslot):
                return Response({'Error': 'No available barber in selected date'})
            
            return Response({f'Barber full timeslot on {dict(BarberTimeslot.DAYS_OF_WEEK).get(date.weekday())} ({date})': full_timeslot})
            
                
        barber_timeslot = BarberTimeslot.objects.get(
            Q(user=id) &
            Q(day_of_week=date.weekday())
        )
        appo = Appointment.objects.filter(
            Q(barber=id) &
            Q(date=date)
        )

        barber_working_hour = barber_timeslot.timeslot
        booked_slot = [a.start_time for a in appo]
        for slot in booked_slot:
            barber_working_hour = barber_working_hour[:slot] + '0' + barber_working_hour[slot + 1:]
            
        return Response({f'Barber timeslot': barber_working_hour})


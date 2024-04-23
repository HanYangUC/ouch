from django.shortcuts import render

# Create your views here.
from . import serializers
from rest_framework import viewsets
from rest_framework.response import Response
from .models import User
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
        q = User.objects.get_queryset()
        
        return Response(str(q))
    

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

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
class LoginView(APIView):
    authentication_class = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        print('heh')
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


from .models import BarberTimeslot
from appointments.models import Appointment
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
            print('created', barber_timeslot)
        else:
            print(Q(date__week_day=(int(day_of_week)+2)%7))
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
                        return Response({'error': 'active booking, cannot update (or cancel the appointment before updating)'})
                    
                
                
                
                barber_timeslot.timeslot = timeslot
                barber_timeslot.save()
                    
            return Response({'updated': 'updated'})
            
        return Response({"a"})
    
    
    def get_timeslotss(self, request, id=None, val_date=None, *args, **kwargs):
        if val_date:
            date = val_date
            if date < datetime.today().date():
                raise Response('cannot be earlier than today')
        else: 
            date = datetime.strptime(request.GET.get('date'), "%d-%m-%Y") or val_date
            if date.date() < datetime.today().date():
                return Response('cannot be earlier than today')
        full_timeslot = []
        
        if not id:
            barber_timeslot = BarberTimeslot.objects.filter(
                Q(day_of_week=date.weekday())
            )
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
                    return Response({'Error': 'no available barber in selected timeslot'})
                else:
                    return Response({f'available on {time}': data})
            
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
        # print(booked_slot, appo)
        for slot in booked_slot:
            barber_working_hour = barber_working_hour[:slot] + '0' + barber_working_hour[slot + 1:]
            
        data = {
            'bab': barber_working_hour
        }
        # print(data['bab'])
            
        return Response({'barber timeslot': barber_working_hour})


    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = serializers.UserTimeslotSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        return Response(serializer.data)
        
    def list(self, request, id=None, val=False, *args, **kwargs):
        queryset = BarberTimeslot.objects.all()
        timeslotlist = []
        serializer = serializers.UserTimeslotSerializer(queryset, many=True)
        for x in serializer.data:
            timeslotlist.append((x['user'], x['day_of_week'], x['available_start'], x['available_end']))
        user_working_hours = get_working_hours(timeslotlist)
        print(user_working_hours)
        if val:
            print(1)
            if id:
                return user_working_hours[id]
            return user_working_hours
            
        if id:
            print(2)
            return Response({id: user_working_hours[id]})
        return Response({"Available timeslots": user_working_hours})
        
    def get_free_slot(self, request, id=None, *args, **kwargs):
        date = datetime.strptime(request.GET.get('date'), "%d-%m-%Y")
        
        if date.date() < datetime.today().date():
            return Response('cannot be earlier than today')
        
        ts = BarberTimeslot.objects.filter(
            Q(user=id) &
            Q(day_of_week=date.weekday())
        )
        appo = Appointment.objects.filter(
            Q(barber=id) &
            Q(date=date)
        )
        barber_working_hour = get_hours([(t.available_start, t.available_end) for t in ts])
        booked_slot = [a.start_time for a in appo]
        
        print(barber_working_hour, booked_slot)
        
        free_hour = set(barber_working_hour) -set(booked_slot)
        '''
            true = booked
            false = available
        '''
        schedule = {hour: hour in booked_slot for hour in barber_working_hour}
        
        # filter by range of date
        # #swapping out
        # if start.weekday() > end.weekday():
        #     start, end = end, start
        # # print(Q(day_of_week__range=[start.weekday(), end.weekday()]))
        # a = BarberTimeslot.objects.filter(
        #     Q(user=id) &
        #     Q(day_of_week__range=[start.weekday(), end.weekday()])
        # )
        
        # for x in a:
        #     qwe.
        
        # test = get_working_hours
        
        return Response({'barber\'s timeslot': schedule})
        # BarberTimeslot.objects.filter

def get_hours(schedule):
    hours = []
    for s in schedule:
        start, end = s
        diff = end - start
        hours.extend(range(start, start+diff))
        hours.sort()
    return hours
        
        
        
        
def get_working_hours(barber_timeslots):
    barber_working_hours = {}
    working_hours = []
    last_barber = None
    day = {}
    last_dow = None
    for data in barber_timeslots:
        current_barber, day_of_week, start, end = data
        if (last_barber and not last_barber == current_barber):
            working_hours = []
            day = {}
        if current_barber == last_barber and not last_dow == day_of_week:
            working_hours = []
        last_dow = day_of_week
        last_barber = current_barber
    
        time_diff = end-start
        working_hours.extend(range(start,start+time_diff))
        working_hours.sort()
        day[day_of_week] = working_hours
        barber_working_hours[current_barber] = day
    print(33)

    return barber_working_hours



from typing import OrderedDict, Any
from rest_framework import serializers

from accounts.models import BarberTimeslot
from .models import Appointment
from datetime import datetime
from accounts.views import TimeslotViewset 
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail
from .utils import send_email

class AppointmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Appointment
        fields = '__all__'
        
    # def to_representation(self, instance: Appointment) -> OrderedDict[str, Any]:
    #     ret = super().to_representation(instance)
    #     # ret['day_of_week'] = instance['date'].weekday() 
    #     return ret
    
    def validate(self, data):
        if self.is_available(data):
            return data
        
        
        
        # appointment_is_available = self.check_availability(data)
        # if appointment_is_available:
        #     return data
    
    def is_available(self, data):
        # print('val1')
        is_working = BarberTimeslot.objects.filter(day_of_week=data['date'].weekday()).exists()
        if not is_working:
            raise serializers.ValidationError({"error": "barber not working on that day"})
        else:
            timeslot = TimeslotViewset.get_timeslots(self, data, id=data['barber'].id, val_date=data['date'])
            
            print('11')
            print(timeslot.data['barber timeslot'][0])
            
            if timeslot.data['barber timeslot'][data['start_time']] == '0':
                raise serializers.ValidationError({"error": "not working on that slot"})
            
            send_email(customer=data['customer'], barber=data['barber'], date=data['date'], start_time=data['start_time'])
            send_email(customer=data['customer'], barber=data['barber'], date=data['date'], start_time=data['start_time'], to_barber=True)
            
            
            return True
    
    # def check_availability(self, data):
    #     barber_available_time = TimeslotViewset.list(self, data, id=data['barber'].id, val=True)
    #     # print(data['date'].weekday(), barber_available_time)
    #     if data['date'].weekday() not in barber_available_time:
    #         # print('not working on that day')
    #         raise serializers.ValidationError({"error":"not working on that day"})
    #     else:
    #         if data['start_time'] not in barber_available_time[data['date'].weekday()]:
    #             # print('not working on that slot')
    #             raise serializers.ValidationError({"error":"not working not the slot"})
                
    #         else:
                
    #             print('working on that slot')
    #             # check if slot taken
    #             appointment_exist = Appointment.objects.filter(barber=data['barber'], start_time=data['start_time']).exists()
    #             if appointment_exist:
    #                 raise serializers.ValidationError({"error":"slot taken"})
    #                 print('slot taken, choose another time')
    #             else:
    #                 print('slot available, proceed')
    #                 subject = 'Appointment booked'
    #                 message = f"Hi {data['customer'].name}, successfully booked for barber ({data['barber'].name}) on {data['date']} @ {data['start_time']}:00."
    #                 email_from = settings.EMAIL_HOST_USER
    #                 recipient_list = [data['customer'].email, ]
    #                 send_mail( subject, message, email_from, recipient_list )
                    
    #                 subject = f"Appointment booked on {data['date']} @ {data['start_time']}:00"
    #                 message = f"Hi {data['barber'].name}, successfully booked from customer ({data['customer'].name}) on {data['date']} @ {data['start_time']}:00.\nPhone: {data['customer'].phone}\nEmail: {data['customer'].email}"
    #                 email_from = settings.EMAIL_HOST_USER
    #                 recipient_list = [data['customer'].email, ]
    #                 send_mail( subject, message, email_from, recipient_list )
                    

    #                 # email
    #                 print(data)
    #                 return True
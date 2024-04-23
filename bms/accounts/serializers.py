from rest_framework import serializers
from .models import User, BarberTimeslot
from django.db.models import Q

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            role=validated_data['role'],
        )
        return user

class UserTimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarberTimeslot
        fields = '__all__'
        
    # def validate(self, data):
    #     if data['available_end'] <= data['available_start']:
    #         raise serializers.ValidationError({"available_end": "available_end should not be same or earlier than available_start"})
    #     if self.is_overlapped(data):
    #         raise serializers.ValidationError({"Input timeslot already exist": 'Please check the timeslot again'})
    #     return data
    
    # def is_overlapped(self, data):
    #     is_exist = BarberTimeslot.objects.filter(
    #         Q(user=data['user']) & 
    #         Q(day_of_week=data['day_of_week']) &
    #         (
    #             Q(available_start__range=(data['available_start']+1, data['available_end'])) | 
    #             Q(available_end__range=(data['available_start']+1, data['available_end']))
    #         )
    #     ).exists()
        
    #     return is_exist
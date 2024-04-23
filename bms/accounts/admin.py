from django.contrib import admin
from .models import User, BarberTimeslot
from rest_framework.authtoken.models import Token as RestToken

# Register your models here.
admin.site.register(User)
admin.site.register(BarberTimeslot)
# admin.site.unregister(RestToken)

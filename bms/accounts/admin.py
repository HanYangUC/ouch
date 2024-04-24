from django.contrib import admin
from .models import User, BarberTimeslot

# Register your models here.
admin.site.register(User)
admin.site.register(BarberTimeslot)

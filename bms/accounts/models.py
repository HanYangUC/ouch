from django.db import models

# Create your models here.
from django.contrib.auth.models import Group, Permission, AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have a valid email address.')
        if not username:
            raise ValueError('Users must have a valid username.')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.role = User.ROLE_CUSTOMER  # Default role
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        user = self.create_user(email, username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.role = User.ROLE_ADMIN
        user.save(using=self._db)
        return user

class User(AbstractUser, PermissionsMixin):
    ROLE_ADMIN = 'ADMIN'
    ROLE_STAFF = 'STAFF'
    ROLE_CUSTOMER = 'CUSTOMER'
    
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_STAFF, 'Staff'),
        (ROLE_CUSTOMER, 'Customer'),
    ]
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='custom_user')
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=18, unique=True)
    phone = models.CharField(max_length=13)
    email = models.EmailField(unique=True) 
    #location?
    area = models.CharField(max_length=50, default='')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Add related_name attributes to avoid clashing with auth.User
    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='custom_user_groups',
    #     blank=True
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='custom_user_permissions',
    #     blank=True
    # )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.role}: {self.username} - {self.id}'

from django.core.validators import MaxValueValidator, MinValueValidator
class BarberTimeslot(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    timeslot = models.CharField(default='000000000000000000000000')

    class Meta:
        ordering = ['user', 'day_of_week']
        unique_together = ('user', 'day_of_week')
        
    def __str__(self):
        return f'{self.user.name} - {dict(self.DAYS_OF_WEEK).get(int(self.day_of_week))}: {self.timeslot}'
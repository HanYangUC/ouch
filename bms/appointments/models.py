from django.db import models
from accounts.models import User

# Create your models here.

class Appointment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    barber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff')
    date = models.DateField()
    start_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_cancelled = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['barber', 'date', 'start_time'], name='unique_appointment')
        ]


    def __str__(self):
        return f'{self.date} - {self.customer.name} - {self.barber.name}: {self.start_time}'
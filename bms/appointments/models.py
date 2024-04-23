from django.db import models
from accounts.models import User

# Create your models here.

class Appointment(models.Model):
    
    TIMESLOT_LIST = (
        (0, '09:00 - 09:30'),
        (1, '09:30 - 10:00'),
        (2, '10:00 - 10:30'),
        (3, '10:30 - 11:00'),
        (4, '11:00 - 11:30'),
        (5, '11:30 - 12:00'),
        (6, '13:00 - 13:30'),
        (7, '13:30 - 14:00'),
        (8, '14:00 - 14:30'),
        (9, '14:30 - 15:00'),
        (10, '15:00 - 15:30'),
        (11, '15:30 - 16:00'),
        (12, '16:00 - 16:30'),
        (13, '16:30 - 17:00'),
        (14, '17:00 - 17:30'),
        (15, '17:30 - 18:00'),
        (16, '18:00 - 18:30'),
        (17, '18:30 - 19:00'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    barber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff')
    date = models.DateField()
    # timeslot = models.IntegerField(choices=TIMESLOT_LIST)
    # timeslot = models.ForeignKey(BarberTimeslot, on_delete=models.CASCADE)
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
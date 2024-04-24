from django.conf import settings
from django.core.mail import send_mail
from appointments.models import Appointment


def send_email(barber, customer, date, start_time, to_barber=False):
    subject = 'Appointment booked'
    email_from = settings.EMAIL_HOST_USER
    if to_barber:
        message = f"Hi {barber.name}, {start_time}:00 on {date} is booked. \nCustomer name: {customer.name}\nPhone Number: {customer.phone}\nEmail: {customer.email}"
        recipient_list = [barber.email ]
    else:
        message = f"Hi {customer.name}, successfully booked for barber ({barber.name}) on {date} @ {start_time}:00."
        recipient_list = [customer.email ]
    send_mail( subject, message, email_from, recipient_list )


def send_email_cancel(appointment: Appointment):
    subject = 'Appointment cancelled'
    email_from = settings.EMAIL_HOST_USER
    message = f"Appointment on {appointment.date}: {appointment.start_time}:00 is cancelled."
    recipient_list = [appointment.barber.email, appointment.customer.email ]
    send_mail( subject, message, email_from, recipient_list )
    
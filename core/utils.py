# utils.py (create this file in the same app directory)

from django.core.mail import send_mail
from django.conf import settings


def send_hire_me_email(hire_me):
    subject = f"Confirmation for {hire_me.name}"
    message = f"""
    Dear {hire_me.name},

    Thank you for your interest in our services. Here are the details of your project:

    Project Details:
    {hire_me.project_details}

    We will get back to you soon to discuss further.

    Best regards,
    Your Company
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [hire_me.email],
        fail_silently=False,
    )


def send_book_call_email(book_call):
    subject = f"Call Booking Confirmation for {book_call.name}"
    message = f"""
    Dear {book_call.name},

    Your call booking has been confirmed.

    Preferred Date: {book_call.preferred_date}
    Preferred Time: {book_call.preferred_time}

    We look forward to speaking with you.

    Best regards,
    Your Company
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [book_call.email],
        fail_silently=False,
    )

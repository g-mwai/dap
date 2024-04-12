import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def generate_random_code():
    return str(random.randint(10000, 99999))

def send_password_reset_email(user, code):
    subject = 'Password Reset Code'
    html_message = render_to_string('email/password_reset_email.html', {'code': code})
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        'from@example.com',
        [user.email],
        html_message=html_message,
    )
"""Celery tasks."""

# Django
import random
import string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Models
from cride.users.models import User, OTP
from cride.rides.models import Ride

# Celery
from .celery import app as celery_app
from celery import shared_task

# Utilities
import jwt
import time
from datetime import timedelta


def generate_code(k):
    """Generate a random k-digit passcode."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))


def gen_otp(user):
    """Create JWT token that the user can use to verify its account."""
    otp = OTP(
        user=user
    )
    while True:
        code = generate_code(8)
        if not OTP.objects.filter(code=code).exists():
            break
    otp.code = code
    otp.save()
    return otp.code


def gen_verification_token(user):
    """Create JWT token that the user can use to verify its account."""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


@celery_app.task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
    """Send account verification link to given user."""
    user = User.objects.get(pk=user_pk)
    verification_token = gen_otp(user)
    subject = 'Welcome @{}! Verify your account to start using Shared Ride'.format(user.username)
    from_email = 'Shared Ride <noreply@sharedrideapp.com>'
    content = render_to_string(
        'emails/users/account_verification.html',
        {'token': verification_token, 'user': user}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()


@celery_app.task(name='disable_finished_rides', run_every=timedelta(minutes=20))
def disable_finished_rides():
    """Disable finished rides."""
    now = timezone.now()
    offset = now + timedelta(minutes=20)

    # Update rides that have already finished
    rides = Ride.objects.filter(
        arrival_date__gte=now,
        arrival_date__lte=offset,
        is_active=True
    )
    rides.update(is_active=False)


@celery_app.task(name='delete_used_otp', run_every=timedelta(days=30))
def clean_otp():
    """Prunes the used OTP instances so that the application
    does not run out of options. Theoretically it shouldn't,
    as there are 36^8 possible combinations with the actual
    configuration. Still, in case the length of the OTP is
    changed for any reason, the number of possible combinations
    may significantly drop (For example, if the length of the OTP
    is changed to 4, it becomes 1679616), which leads to a higher
    chance of collision."""
    otp_set = OTP.objects.filter(verified=True)
    otp_set.delete()

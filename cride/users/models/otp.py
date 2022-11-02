"""OTP (One-time passcode) models."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class OTP(CRideModel):
    """OTP Model.

    This model represents a one-time passcode which will be used to verify user accounts
    when the user uses the passcode they receive in their sign-up email. All passcodes are
    rendered useless when verified, but still they remain persisted."""
    modified = None
    code = models.CharField('OTP that was sent to the user.', max_length=10, unique=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    verified = models.BooleanField('OTP has been verified?', default=False)

    def __str__(self):
        return f'OTP sent to {self.user.username}'

    class Meta:
        ordering = ['-created']

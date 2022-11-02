"""Follow model."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Follow(CRideModel):
    """Follow model.

    This class represents the relationship between users that follow each other.
    Inherits from Orchestrator Model to keep useful stats."""
    updated = None
    follower = models.ForeignKey(
        'users.User',
        related_name='user_follower',
        on_delete=models.CASCADE,
        help_text='User who followed.'
    )
    followed = models.ForeignKey(
        'users.User',
        related_name='followed_user',
        on_delete=models.CASCADE,
        help_text='User who was followed.'
    )

    class Meta:
        ordering = ['-created', ]
        unique_together = ('follower', 'followed',)

    def __str__(self):
        return f'{self.follower} followed {self.followed}'

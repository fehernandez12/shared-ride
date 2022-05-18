"""Circle model."""

# Django
import random
import string
from django.db import models
from django.utils.text import slugify

# Utilities
from cride.utils.models import CRideModel


class Circle(CRideModel):
    """Circle model.

    A circle is a private group where rides are offered and taken
    by its members. To join a circle a user must receive an unique
    invitation code from an existing circle member.
    """

    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40, blank=True)

    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)

    members = models.ManyToManyField(
        'users.User',
        through='circles.Membership',
        through_fields=('circle', 'user')
    )

    # Stats
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(
        'verified circle',
        default=False,
        help_text='Verified circles are also known as official communities.'
    )

    is_public = models.BooleanField(
        default=True,
        help_text='Public circles are listed in the main page so everyone know about their existence.'
    )

    is_limited = models.BooleanField(
        'limited',
        default=False,
        help_text='Limited circles can grow up to a fixed number of members.'
    )
    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='If circle is limited, this will be the limit on the number of members.'
    )

    def __str__(self):
        """Return circle name."""
        return self.name

    def random_string_generator(size: int):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        """Override save method to generate a unique slug_name."""
        self.slug_name = slugify(self.name) + self.random_string_generator(6) if not self.slug_name else self.slug_name
        super().save(*args, **kwargs)

    class Meta(CRideModel.Meta):
        """Meta class."""

        ordering = ['-rides_taken', '-rides_offered']

from django.db import models

from cride.utils.models import CRideModel


class Contact(CRideModel):
    name = models.CharField("contact name", max_length=50)
    email = models.EmailField("email address")
    message = models.TextField("message", max_length=500)

    class Meta:
        ordering = ["-created"]

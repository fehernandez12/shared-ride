from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from cride.blog.serializers.contact import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        permissions = [AllowAny]
        return [p() for p in permissions]

    throttle_classes = (AnonRateThrottle,)
    serializer_class = ContactSerializer

from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status

from cride.blog.serializers.contact import ContactSerializer


class ContactViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def get_permissions(self):
        permissions = [AllowAny]
        return [p() for p in permissions]

    throttle_classes = (AnonRateThrottle,)
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        """Handle contact creation."""
        serializer = ContactSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()
        data = ContactSerializer(contact).data
        return Response(data, status=status.HTTP_201_CREATED)

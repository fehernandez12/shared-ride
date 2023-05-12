from rest_framework import serializers
from cride.blog.models.contact import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        read_only_fields = ("created", "modified")

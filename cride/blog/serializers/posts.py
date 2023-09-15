from rest_framework import serializers
from cride.blog.models.contact import Contact

from cride.blog.models.posts import Post, Status
from taggit.serializers import TagListSerializerField, TaggitSerializer


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        exclude = ("id",)


class ListPostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    published = serializers.DateTimeField(required=False)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = (
            "id",
            "body",
        )
        read_only_fields = ("published", "created", "modified")


class RecentListPostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    abstract = serializers.CharField(required=True)
    published = serializers.DateTimeField(required=False)

    class Meta:
        model = Post
        exclude = ("id", "views", "status", "body",)
        read_only_fields = ("published", "created", "modified")


class RelatedPostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    abstract = serializers.CharField(required=True)
    published = serializers.DateTimeField(required=False)

    class Meta:
        model = Post
        exclude = ("id", "views", "status", "body",)
        read_only_fields = ("published", "created", "modified")


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    abstract = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    published = serializers.DateTimeField(required=False)
    status = StatusSerializer(read_only=True)
    views = serializers.IntegerField(read_only=True)
    related = RelatedPostSerializer(read_only=True, many=True)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        exclude = ("id",)
        read_only_fields = ("published", "created", "modified", "tags")

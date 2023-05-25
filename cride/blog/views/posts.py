from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from taggit.models import Tag

from cride.blog.models.posts import Post
from cride.blog.serializers.posts import (
    ListPostSerializer,
    PostSerializer,
    RecentListPostSerializer,
)


class PostsViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    lookup_field = "slug"
    queryset = Post.posted.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ListPostSerializer
        elif self.action == "recent":
            return RecentListPostSerializer
        return PostSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [AllowAny]
        return [p() for p in permissions]

    def list(self, request):
        """Handle list action."""
        queryset = Post.posted.all()
        tag_slug = self.request.query_params.get("tag")
        if tag_slug is not None:
            try:
                tag = Tag.objects.get(slug=tag_slug)
                queryset = queryset.filter(tags__name__in=[tag])
                serializer = PostSerializer(queryset, many=True)
                return Response(serializer.data)
            except Tag.DoesNotExist:
                queryset = Post.posted.none()
        search_q = self.request.query_params.get("q")
        if search_q is not None:
            search_vector = SearchVector("title", weight="A") + SearchVector(
                "body", weight="B"
            )
            if len(search_q) > 3:
                search_query = SearchQuery(search_q)
                queryset = (
                    queryset.annotate(
                        search=search_vector,
                        rank=SearchRank(search_vector, search_query),
                    )
                    .filter(search=search_q)
                    .filter(rank__gte=0.3)
                    .order_by("-rank")
                )
            else:
                queryset = Post.posted.none()
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)
        serializer = ListPostSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Increase view counter for the blog post retrieved."""
        post = self.get_object()
        post.views += 1
        post.save()
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def popular(self, request, *args, **kwargs):
        """Return the most popular posts."""
        count = self.request.query_params.get("count", 12)
        queryset = Post.posted.all().order_by("-views")[:count]
        serializer = RecentListPostSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recent(self, request, *args, **kwargs):
        """Return the last 5 published posts."""
        count = self.request.query_params.get("count", 12)
        queryset = Post.posted.all()[:count]
        serializer = RecentListPostSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def related(self, request, *args, **kwargs):
        """Return similar posts to the current one."""
        post = self.get_object()
        post_tags_ids = post.tags.values_list("id", flat=True)
        related_posts = Post.posted.filter(tags__in=post_tags_ids).exclude(id=post.id)
        related_posts = related_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-published"
        )[:4]
        serializer = RecentListPostSerializer(related_posts, many=True)
        return Response(serializer.data)

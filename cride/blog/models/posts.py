from django.db import models
from cride.utils.models import CRideModel
from taggit.managers import TaggableManager


class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    """Manager for published posts."""

    def get_queryset(self):
        """Return published posts."""
        return super(PublishedManager, self).get_queryset().filter(status__name='Published')


class Post(CRideModel):
    """Blog post model."""
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, unique_for_date='published')
    body = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    posted = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title

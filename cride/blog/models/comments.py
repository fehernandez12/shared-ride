from django.db import models
from cride.utils.models import CRideModel


class Comment(CRideModel):
    """Comment model."""
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    comment = models.TextField()
    active = models.BooleanField(default=True)

    class Meta(CRideModel.Meta):
        """Meta class."""
        ordering = ['-created']

    def __str__(self):
        """Return comment name and post."""
        return 'Comment by {} on {}'.format(self.name, self.post)

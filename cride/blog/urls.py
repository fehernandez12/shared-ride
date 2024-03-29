"""Posts URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import posts as posts_views
from .views import contact as contact_views

router = DefaultRouter()
router.register(r"posts", posts_views.PostsViewSet, basename="posts")
router.register(r"contact", contact_views.ContactViewSet, basename="contact")

urlpatterns = [path("", include(router.urls))]

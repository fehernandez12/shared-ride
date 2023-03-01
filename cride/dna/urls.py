"""DNA URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import ProteinViewSet

router = DefaultRouter()
router.register(r'dna', ProteinViewSet, basename='dna')

urlpatterns = [
    path('', include(router.urls))
]

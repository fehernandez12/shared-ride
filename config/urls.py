"""Main URLs module."""

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

admin.site.site_header = 'Shared Ride Administration'
admin.site.site_title = 'Shared Ride administration site'

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    path('api/', include(('cride.circles.urls', 'circles'), namespace='circles')),
    path('api/', include(('cride.users.urls', 'users'), namespace='users')),
    path('api/', include(('cride.rides.urls', 'rides'), namespace='rides')),
    path('api/', include(('cride.dna.urls', 'dna'), namespace='dna')),
    path('api/blog/', include(('cride.blog.urls', 'blog'), namespace='blog')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

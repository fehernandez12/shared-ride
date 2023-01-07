"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from cride.users.models import User, Profile, OTP


class CustomUserAdmin(UserAdmin):
    """User model admin."""
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_client')
    list_filter = ('is_client', 'is_staff', 'created', 'modified')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ('user', 'reputation', 'rides_taken', 'rides_offered')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('reputation',)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    """OTP model admin"""
    list_display = ('user', 'verified')
    search_fields = ('user__username',)
    list_filter = ('verified',)


admin.site.register(User, CustomUserAdmin)

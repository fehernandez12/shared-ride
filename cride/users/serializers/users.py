"""Users serializers."""

# Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator

# Models
from cride.users.models import User, Profile

# Tasks
from cride.taskapp.tasks import send_confirmation_email
from cride.users.models.otp import OTP

# Serializers
from cride.users.serializers.profiles import ProfileModelSerializer

# Utilities
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
        )


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle sign up data validation and user/profile creation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex])

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False, is_client=True)
        Profile.objects.create(user=user)
        send_confirmation_email.delay(user_pk=user.pk)
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        refresh = RefreshToken.for_user(self.context['user'])
        return self.context['user'], str(refresh), str(refresh.access_token)


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""
    otp = serializers.CharField()
    username = serializers.CharField()

    def validate_otp(self, data):
        """Verify OTP."""
        otp_instance = OTP.objects.filter(code=data)
        if not otp_instance:
            raise serializers.ValidationError('Invalid verification code.')
        if otp_instance.first().verified:
            raise serializers.ValidationError('Account has been verified already.')
        self.context['verification_otp'] = otp_instance.first().code
        return data

    def validate_username(self, data):
        """Verify Username."""
        user = User.objects.filter(username=data).first()
        if not user:
            raise serializers.ValidationError('Invalid username.')
        if user.is_verified:
            raise serializers.ValidationError('Account has been verified already.')
        self.context['username'] = user.username
        return data

    def save(self):
        """Update user's verified status."""
        code = self.context['verification_otp']
        otp = OTP.objects.get(code=code)
        otp.verified = True
        otp.save()
        user = User.objects.get(username=self.context['username'])
        user.is_verified = True
        user.save()


class PasswordChangeSerializer(serializers.Serializer):
    """Handles password change data. Validates the old password and
    validates the new passwords and finally changes it."""
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password_confirmation = serializers.CharField()

    def validate_old_password(self, data):
        user = self.instance
        if not user.check_password(data):
            raise serializers.ValidationError("Incorrect password.")
        return data

    def validate(self, data):
        passwd = data['new_password']
        passwd_conf = data['new_password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        self.context['password'] = passwd
        return data

    def save(self):
        new_passwd = self.validated_data['new_password']
        user = self.instance
        user.set_password(new_passwd)
        user.save()
        return user

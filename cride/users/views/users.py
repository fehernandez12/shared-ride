"""Users views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from cride.users.permissions import IsAccountOwner

# Serializers
from cride.users.serializers.profiles import ProfileModelSerializer
from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers import (
    AccountVerificationSerializer,
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer
)

# Models
from cride.users.models import User
from cride.circles.models import Circle
from cride.users.serializers.users import PasswordChangeSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User view set.

    Handle sign up, login and account verification.
    """

    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permissions based on action.
        Actions are described as the viewset's native
        method-mapped actions (create, update, partial_update,
        retrieve, list, destroy), or any custom action
        defined by the @action decorator."""
        if self.action in ['signup', 'login', 'verify', 'token_info']:
            permissions = [AllowAny]
        elif self.action in ['update', 'partial_update', 'profile']:
            permissions = [IsAuthenticated, IsAccountOwner]
        elif self.action in ['retrieve', ]:
            permissions = [IsAuthenticated]
        else:
            permissions = [AllowAny]
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in.

        Returns the access token for the user, which represents
        its account when performing any other request while
        logged in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, refresh, access_token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': {
                'access_token': access_token,
                'refresh_token': refresh,
            }
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations, now go share some rides!'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Update profile data.

        NOTE: This method is different from the update action,
        as in, it updates only the information for the user's
        profile. User info cannot be edited via this method
        (returns a 400)."""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)

    @action(detail=True, methods=['post'])
    def password(self, request, *args, **kwargs):
        """Update the user's password.

        User should be logged out from the frontend
        when the password is changed, so that a new
        access_token is generated when they log back
        in."""
        user = self.get_object()
        serializer = PasswordChangeSerializer(
            user,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'user': UserModelSerializer(user).data
        }
        return Response(data, status=status.HTTP_202_ACCEPTED)

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )
        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        return response

    def update(self, request, *args, **kwargs):
        """Update user data.

        Profile data cannot be edited via this method.
        To do it, the profile action must be used instead."""
        user = self.get_object()
        partial = request.method == 'PATCH'
        serializer = UserModelSerializer(
            user,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_202_ACCEPTED)

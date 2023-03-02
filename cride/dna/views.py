from cride.dna.serializers import ProteinSerializer
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ProteinViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ProteinSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        """Handle protein creation from DNA string."""
        serializer = ProteinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        protein = serializer.save()
        return Response(protein, status=status.HTTP_201_CREATED)

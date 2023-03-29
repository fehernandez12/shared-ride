from cride.dna.serializers import ProteinSerializer, DNASerializer, ScoreSerializer
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action


class ProteinViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ProteinSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [AllowAny]
        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        """Handle protein creation from DNA string."""
        serializer = DNASerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        protein = serializer.save()
        return Response(protein, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def protein(self, request, *args, **kwargs):
        """Handle protein creation from DNA string."""
        serializer = ProteinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        protein = serializer.save()
        return Response(protein, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def score(self, request, *args, **kwargs):
        """Handle score from comparing 2 DNA strings."""
        serializer = ScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_201_CREATED)

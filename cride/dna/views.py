from cride.dna.serializers import ProteinSerializer
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response


class ProteinViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ProteinSerializer

    def create(self, request, *args, **kwargs):
        """Handle protein creation from DNA string."""
        serializer = ProteinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        protein = serializer.save()
        return Response(protein, status=status.HTTP_201_CREATED)

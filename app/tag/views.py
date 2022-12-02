from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from core.models import Tag
from tag.serializers import TagSerializer


@extend_schema(auth=[{}])
class TagViewSet(viewsets.ModelViewSet):
    """Manage categories in the database"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ["get", "post", "delete", "put"]

    def get_queryset(self):
        return self.queryset.filter().order_by("-name")

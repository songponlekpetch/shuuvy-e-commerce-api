from rest_framework import viewsets

from core.models import Tag
from tag.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    """Manage categories in the database"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ["get", "post", "delete", "put"]

    def get_queryset(self):
        return self.queryset.filter().order_by("-name")

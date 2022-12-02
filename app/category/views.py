from rest_framework import viewsets

from core.models import Category
from category.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Manage categories in the database"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ["get", "post", "delete", "put"]

    def get_queryset(self):
        return self.queryset.filter().order_by("-name")

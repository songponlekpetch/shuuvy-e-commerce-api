from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from core.models import Brand
from brand.serializers import BrandSerializer


@extend_schema(auth=[{}])
class BrandViewSet(viewsets.ModelViewSet):
    """Manage bands in the database"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    http_method_names = ["get", "post", "delete", "put"]

    def get_queryset(self):
        return self.queryset.filter().order_by("-name")

from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from drf_spectacular.utils import extend_schema

from core.models import Brand
from brand.serializers import BrandSerializer, UploadBrandSerializer


@extend_schema(auth=[{}])
class BrandViewSet(viewsets.ModelViewSet):
    """Manage bands in the database"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    http_method_names = ["get", "post", "delete", "put"]
    pagination_class = LimitOffsetPagination
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter().order_by("-name")

    @extend_schema(request={"multipart/form-data": UploadBrandSerializer})
    @action(detail=True, methods=["post"], url_path="upload-image")
    def upload_image(self, request, id=None):
        """Upload an image to a brand"""
        brand = Brand.objects.get(id=id)
        serializer = UploadBrandSerializer(data=dict(
            image_file=request.FILES.get("image_file")
        ))
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        brand_image = serializer.create(brand)

        return Response(brand_image.data, status=status.HTTP_200_OK)

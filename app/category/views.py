from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from core.models import Category
from category.serializers import CategorySerializer, UploadCategorySerializer


@extend_schema(auth=[{}])
class CategoryViewSet(viewsets.ModelViewSet):
    """Manage categories in the database"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ["get", "post", "delete", "put"]
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter().order_by("-name")

    @extend_schema(request={"multipart/form-data": UploadCategorySerializer})
    @action(detail=True, methods=["post"], url_path="upload-image")
    def upload_image(self, request, id=None):
        """Upload an image to a category"""
        category = Category.objects.get(id=id)
        serializer = UploadCategorySerializer(data=dict(
            image_file=request.FILES.get("image_file")
        ))
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        category = serializer.create(category)

        return Response(category.data, status=status.HTTP_200_OK)

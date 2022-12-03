from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter, OpenApiTypes)

from core.models import Subcategory
from subcategory.serializers import SubcategorySerializer, UploadSubcategorySerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "categories",
                OpenApiTypes.STR,
                description="Comma separated list of category IDs to filter",
            )
        ]
    )
)
@extend_schema(auth=[{}])
class SubcategoryViewSet(viewsets.ModelViewSet):
    """Manage subcategories in the database"""
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    http_method_names = ["get", "post", "delete", "put"]

    def _params_to_ints(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        categories = self.request.query_params.get('categories', None)
        queryset = self.queryset

        if categories:
            category_ids = self._params_to_ints(categories)
            queryset = queryset.filter(category__id__in=category_ids)

        return queryset.filter().order_by("-name")

    @extend_schema(request={"multipart/form-data": UploadSubcategorySerializer})
    @action(detail=True, methods=["post"], url_path="upload-image")
    def upload_image(self, request, id=None):
        """Upload an image to a subcategory"""
        subcategory = Subcategory.objects.get(id=id)
        serializer = UploadSubcategorySerializer(data=dict(
            image_file=request.FILES.get("image_file")
        ))
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        subcategory = serializer.create(subcategory)

        return Response(subcategory.data, status=status.HTTP_200_OK)

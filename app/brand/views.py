from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes

from core.models import Brand
from brand.serializers import BrandSerializer, UploadBrandSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "keyword",
                OpenApiTypes.STR,
                description="Keyword to search",
            ),
            OpenApiParameter(
                "tags",
                OpenApiTypes.STR,
                description="Comma separated list of tag IDs to filter",
            )
        ]
    )
)
@extend_schema(auth=[{}])
class BrandViewSet(viewsets.ModelViewSet):
    """Manage bands in the database"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    http_method_names = ["get", "post", "delete", "put"]
    lookup_field = "id"

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        queryset = self.queryset

        keyword = self.request.query_params.get('keyword', None)
        tags = self.request.query_params.get('tags', None)

        if keyword:
            queryset = queryset.filter(name__icontains=keyword)

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.filter().order_by("-priority", "-followers", "-name")

    def create(self, request):
        serializer = BrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        brand = serializer.save()

        return Response(BrandSerializer(brand).data, status=status.HTTP_201_CREATED)

    def update(self, request, id):
        serializer = BrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        brand = serializer.update(id, serializer.validated_data)

        return Response(BrandSerializer(brand).data, status=status.HTTP_200_OK)

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

from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from rest_framework.parsers import MultiPartParser, JSONParser

from core.models import Product, ProductImage, ProductSize, ProductColor, ProductModel
from product.serializers import (
    ProductSerializer,
    ProductImageSerializer,
    ProductSizeSerializer,
    ProductColorSerializer,
    ProductModelSerializer,
    EditProductImageSerializer,
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "keyword",
                OpenApiTypes.STR,
                description="Keyword to search",
            ),
            OpenApiParameter(
                "brands",
                OpenApiTypes.STR,
                description="Comma separated list of brand IDs to filter",
            ),
            OpenApiParameter(
                "categories",
                OpenApiTypes.STR,
                description="Comma separated list of category IDs to filter",
            ),
            OpenApiParameter(
                "subcategories",
                OpenApiTypes.STR,
                description="Comma separated list of subcategory IDs to filter",
            ),
            OpenApiParameter(
                "tags",
                OpenApiTypes.STR,
                description="Comma separated list of tag IDs to filter",
            )
        ]
    )
)
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    parser_classes = [JSONParser]
    http_method_names = ["get", "post", "delete", "put"]
    lookup_field = "id"

    def create(self, request):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

    def update(self, request, id):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.update(id, serializer.validated_data)

        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', None)
        brands = self.request.query_params.get('brands', None)
        categories = self.request.query_params.get('categories', None)
        subcategories = self.request.query_params.get('subcategories', None)
        tags = self.request.query_params.get('tags', None)
        queryset = self.queryset

        if keyword:
            queryset = queryset.filter(name__icontains=keyword)

        if brands:
            brand_ids = self._params_to_ints(brands)
            queryset = queryset.filter(brand__id__in=brand_ids)

        if categories:
            category_ids = self._params_to_ints(categories)
            queryset = queryset.filter(category__id__in=category_ids)

        if subcategories:
            subcategory_ids = self._params_to_ints(subcategories)
            queryset = queryset.filter(subcategory__id__in=subcategory_ids)

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.filter().order_by("-name", "-created_at").distinct()


@extend_schema_view(
    create=extend_schema(request={"multipart/form-data": ProductImageSerializer}),
    update=extend_schema(request={"application/json": EditProductImageSerializer}),
)
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    http_method_names = ["get", "post", "delete", "put"]
    parser_classes = [MultiPartParser, JSONParser]
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        product = Product.objects.get(id=product_id)

        return self.queryset.filter(product=product)

    def create(self, request, product_id):
        serializer = ProductImageSerializer(data=dict(
            image_file=request.FILES.get("image_file"),
            is_main=request.POST.get("is_main")))
        product = Product.objects.get(id=product_id)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_image = serializer.create(product)

        return Response(product_image.data, status=status.HTTP_201_CREATED)

    def update(self, request, product_id, id):
        product_image = self.get_object()
        serializer = EditProductImageSerializer(product_image, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(product_image, serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductSizeViewSet(viewsets.ModelViewSet):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer
    http_method_names = ["get", "post", "delete", "put"]

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        product = Product.objects.get(id=product_id)

        return self.queryset.filter(product=product)

    def create(self, request, product_id):
        product = Product.objects.get(id=product_id)
        serializer = ProductSizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_size = serializer.create(product)

        return Response(ProductSizeSerializer(product_size).data, status=status.HTTP_201_CREATED)

    def update(self, request, product_id, pk=None):
        product = Product.objects.get(id=product_id)
        serializer = ProductSizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_size = serializer.update(pk, serializer.validated_data)

        return Response(ProductSizeSerializer(product_size).data, status=status.HTTP_200_OK)

    def destroy(self, request, product_id, pk=None):
        product_size = ProductSize.objects.get(id=pk)
        product_size.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductColorViewSet(viewsets.ModelViewSet):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer
    http_method_names = ["get", "post", "delete", "put"]

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        product = Product.objects.get(id=product_id)

        return self.queryset.filter(product=product)

    def create(self, request, product_id):
        product = Product.objects.get(id=product_id)
        serializer = ProductColorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_color = serializer.create(product)

        return Response(ProductColorSerializer(product_color).data, status=status.HTTP_201_CREATED)

    def update(self, request, product_id, pk=None):
        product = Product.objects.get(id=product_id)
        serializer = ProductColorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_color = serializer.update(pk, serializer.validated_data)

        return Response(ProductColorSerializer(product_color).data, status=status.HTTP_200_OK)

    def destroy(self, request, product_id, pk=None):
        product_color = ProductColor.objects.get(id=pk)
        product_color.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
    http_method_names = ["get", "post", "delete", "put"]

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        product = Product.objects.get(id=product_id)

        return self.queryset.filter(product=product)

    def create(self, request, product_id):
        product = Product.objects.get(id=product_id)
        serializer = ProductModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_model = serializer.create(product)

        return Response(ProductModelSerializer(product_model).data, status=status.HTTP_201_CREATED)

    def update(self, request, product_id, pk=None):
        product = Product.objects.get(id=product_id)
        serializer = ProductModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_model = serializer.update(pk, serializer.validated_data)

        return Response(ProductModelSerializer(product_model).data, status=status.HTTP_200_OK)

    def destroy(self, request, product_id, pk=None):
        product_model = ProductModel.objects.get(id=pk)
        product_model.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
import uuid

from rest_framework import serializers

from core.services.digitalocean_service import DigitalOceanService
from core.configs import (
    PRODUCTS_FOLDER,
    DIGITAL_OCEAN_SETTINGS,
    NO_MAX_UPLOAD_IMAGE)
from core.serializers import BaseSerializer
from core.models import (
    Product,
    ProductImage,
    ProductColor,
    ProductSize,
    ProductModel,
    Brand,
    Promotion,
    Category,
    Subcategory,
    Tag)
from brand.serializers import BrandSerializer
from promotion.serializers import PromotionSerializer
from category.serializers import CategorySerializer
from subcategory.serializers import SubcategorySerializer
from tag.serializers import TagSerializer


class UpdateMixin(serializers.ModelSerializer):
    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        no_update_fields = getattr(self.Meta, "no_update_fields", None)

        if self.instance and no_update_fields:
            for field in no_update_fields:
                kwargs.setdefault(field, {})
                kwargs[field]["read_only"] = True

        return kwargs


class EditProductImageSerializer(BaseSerializer):
    class Meta:
        model = ProductImage
        fields = BaseSerializer.Meta.fields + ("path", "is_main",)
        read_only_fields = BaseSerializer.Meta.read_only_fields + ("path",)


class ProductImageSerializer(UpdateMixin, BaseSerializer):
    image_file = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = ProductImage
        fields = BaseSerializer.Meta.fields + ("image_file", "path", "is_main",)
        read_only_fields = BaseSerializer.Meta.read_only_fields + ("path",)
        no_update_fields = ("image_file",)

    def create(self, product):
        """Create a new image"""
        data = self.validated_data

        if product.product_images.count() >= NO_MAX_UPLOAD_IMAGE:
            raise serializers.ValidationError(
                f"Maximum number of images reached [{NO_MAX_UPLOAD_IMAGE} images]")

        image_format = data["image_file"].name.split(".")[-1]
        if image_format not in ["jpg", "jpeg", "png"]:
            raise serializers.ValidationError(
                f"Invalid image format [{image_format}]")

        digital_ocean_service = DigitalOceanService(**DIGITAL_OCEAN_SETTINGS)
        storage_path = f"{PRODUCTS_FOLDER}/{product.id}/{uuid.uuid4().hex}.{image_format}"
        storage_path = digital_ocean_service.upload_file_to_storage(file=data["image_file"], storage_path=storage_path)

        product_image = ProductImage.objects.create(path=storage_path, is_main=data["is_main"])
        product_image.save()

        product.product_images.add(product_image)

        return ProductImageSerializer(product_image)


class ProductColorSerializer(BaseSerializer):
    """Serializer for product color objects"""
    product_image = ProductImageSerializer(read_only=True)
    product_image_id = serializers.IntegerField(write_only=True)

    class Meta(BaseSerializer.Meta):
        model = ProductColor
        fields = BaseSerializer.Meta.fields + ("name", "description", "code", "product_image", "product_image_id",)

    def create(self, product):
        """Create a new color"""
        data = self.validated_data
        product_image = ProductImage.objects.get(id=data["product_image_id"])
        product_color = ProductColor.objects.create(name=data["name"], code=data["code"], product_image=product_image)
        product_color.save()

        product.product_colors.add(product_color)

        return product_color

    def update(self, id, validated_data):
        """Update an existing color"""
        product_color = ProductColor.objects.get(id=id)
        product_color.name = validated_data["name"]
        product_color.code = validated_data["code"]

        product_image = ProductImage.objects.get(id=validated_data["product_image_id"])
        if product_image:
            product_color.product_image = product_image
            product_color.save()
        else:
            raise serializers.ValidationError("Product image not found")

        return product_color


class ProductSizeSerializer(BaseSerializer):
    """Serializer for product size objects"""

    class Meta(BaseSerializer.Meta):
        model = ProductSize
        fields = BaseSerializer.Meta.fields + ("name",)

    def create(self, product):
        """Create a new size"""
        data = self.validated_data
        product_size = ProductSize.objects.create(name=data["name"])
        product_size.save()

        product.product_sizes.add(product_size)

        return product_size

    def update(self, id, validated_data):
        """Update an existing size"""
        product_size = ProductSize.objects.get(id=id)
        product_size.name = validated_data["name"]
        product_size.save()

        return product_size


class ProductModelSerializer(BaseSerializer):
    """Serializer for product model objects"""
    product_color = ProductColorSerializer(read_only=True)
    product_color_id = serializers.IntegerField(write_only=True)
    product_size = ProductSizeSerializer(read_only=True)
    product_size_id = serializers.IntegerField(write_only=True)

    class Meta(BaseSerializer.Meta):
        model = ProductModel
        fields = BaseSerializer.Meta.fields + (
            "name",
            "product_color_id",
            "product_color",
            "product_size_id",
            "product_size",
            "price",
            "stock_quantity",
            "sale_quantity",)
        read_only_fields = BaseSerializer.Meta.read_only_fields + ("sale_quantity",)

    def _get_product_color(self, product_color_id, product_model):
        product_color = ProductColor.objects.get(id=product_color_id)
        if not product_color:
            raise serializers.ValidationError("Product color not found")

        product_model.product_color = product_color

    def _get_product_size(self, product_size_id, product_model):
        product_size = ProductSize.objects.get(id=product_size_id)
        if not product_size:
            raise serializers.ValidationError("Product size not found")

        product_model.product_size = product_size

    def create(self, product):
        """Create a new model"""
        data = self.validated_data
        product_color_id = data.pop("product_color_id")
        product_size_id = data.pop("product_size_id")

        product_model = ProductModel(**data)
        self._get_product_color(product_color_id, product_model)
        self._get_product_size(product_size_id, product_model)
        product_model.save()

        product.product_models.add(product_model)

        return product_model

    def update(self, id, validated_data):
        """Update an existing model"""
        data = validated_data
        product_color_id = data.pop("product_color_id")
        product_size_id = data.pop("product_size_id")

        product_model = ProductModel.objects.get(id=id)

        if data["name"]:
            product_model.name = data["name"]
        if data["price"]:
            product_model.price = data["price"]
        if data["stock_quantity"]:
            product_model.stock_quantity = data["stock_quantity"]

        self._get_product_color(product_color_id, product_model)
        self._get_product_size(product_size_id, product_model)
        product_model.save()

        return product_model

    def increase_sale_quantity(self, id):
        """Add sale quantity to a product model"""
        product_model = ProductModel.objects.get(id=id)
        product_model.sale_quantity += 1
        product_model.save()

        return product_model


class ProductSerializer(BaseSerializer):
    """Serializer for product objects"""
    brand_id = serializers.IntegerField(write_only=True)
    brand = BrandSerializer(read_only=True)
    promotion_id = serializers.IntegerField(write_only=True, allow_null=True)
    promotion = PromotionSerializer(read_only=True)
    category_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    categories = CategorySerializer(read_only=True, many=True)
    subcategory_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    subcategories = SubcategorySerializer(read_only=True, many=True)
    tag_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    tags = TagSerializer(read_only=True, many=True)
    product_images = ProductImageSerializer(read_only=True, many=True)
    product_colors = ProductColorSerializer(read_only=True, many=True)
    product_sizes = ProductSizeSerializer(read_only=True, many=True)
    product_models = ProductModelSerializer(read_only=True, many=True)

    class Meta(BaseSerializer.Meta):
        model = Product
        fields = BaseSerializer.Meta.fields + (
            "name",
            "description",
            "url",
            "status",
            "min_price",
            "max_price",
            "brand_id",
            "brand",
            "promotion_id",
            "promotion",
            "category_ids",
            "categories",
            "subcategory_ids",
            "subcategories",
            "tag_ids",
            "tags",
            "product_images",
            "product_colors",
            "product_sizes",
            "product_models",
            "click_count",)
        read_only_fields = BaseSerializer.Meta.read_only_fields + ("click_count",)

    def _get_or_create_band(self, brand_id, product):
        band = Brand.objects.get(id=brand_id)
        product.brand = band

    def _get_or_create_promotion(self, promotion_id, product):
        if promotion_id:
            promotion = Promotion.objects.get(id=promotion_id)
            product.promotion = promotion

    def _get_or_create_categories(self, category_ids, product):
        if category_ids:
            for category_id in category_ids:
                category = Category.objects.get(id=category_id)
                product.categories.add(category)

    def _get_or_create_subcategories(self, subcategory_ids, product):
        if subcategory_ids:
            for subcategory_id in subcategory_ids:
                subcategory = Subcategory.objects.get(id=subcategory_id)
                product.subcategories.add(subcategory)

    def _get_or_create_tags(self, tag_ids, product):
        if tag_ids:
            for tag_id in tag_ids:
                tag = Tag.objects.get(id=tag_id)
                product.tags.add(tag)

    def create(self, validated_data):
        """Create a new product"""
        brand_id = validated_data.pop("brand_id", None)
        promotion_id = validated_data.pop("promotion_id", None)
        category_ids = validated_data.pop("category_ids", [])
        subcategory_ids = validated_data.pop("subcategory_ids", [])
        tag_ids = validated_data.pop("tag_ids", [])

        product = Product.objects.create(**validated_data)
        self._get_or_create_band(brand_id, product)
        self._get_or_create_promotion(promotion_id, product)
        self._get_or_create_categories(category_ids, product)
        self._get_or_create_subcategories(subcategory_ids, product)
        self._get_or_create_tags(tag_ids, product)
        product.save()

        return product

    def update(self, pk, validated_data):
        """Update a product"""
        product = Product.objects.get(pk=pk)
        brand_id = validated_data.pop("brand_id", None)
        promotion_id = validated_data.pop("promotion_id", None)
        category_ids = validated_data.pop("category_ids", [])
        subcategory_ids = validated_data.pop("subcategory_ids", [])
        tag_ids = validated_data.pop("tag_ids", [])
        product = super().update(product, validated_data)

        if brand_id:
            self._get_or_create_band(brand_id, product)

        if promotion_id:
            self._get_or_create_promotion(promotion_id, product)

        if category_ids:
            self._get_or_create_categories(category_ids, product)

        if subcategory_ids:
            self._get_or_create_subcategories(subcategory_ids, product)

        if tag_ids:
            self._get_or_create_tags(tag_ids, product)

        product.save()

        return product


class UploadProductImageSerializer(serializers.Serializer):
    """Serializer for uploading images to products"""
    image_file = serializers.ImageField()
    is_main = serializers.BooleanField(default=False)

    def create(self, product):
        """Create a new image"""
        data = self.validated_data

        if product.product_images.count() >= NO_MAX_UPLOAD_IMAGE:
            raise serializers.ValidationError(
                f"Maximum number of images reached [{NO_MAX_UPLOAD_IMAGE} images]")

        image_format = data["image_file"].name.split(".")[-1]
        if image_format not in ["jpg", "jpeg", "png"]:
            raise serializers.ValidationError(
                f"Invalid image format [{image_format}]")

        digital_ocean_service = DigitalOceanService(**DIGITAL_OCEAN_SETTINGS)
        storage_path = f"{PRODUCTS_FOLDER}/{product.id}/{uuid.uuid4().hex}.{image_format}"
        storage_path = digital_ocean_service.upload_file_to_storage(file=data["image_file"], storage_path=storage_path)

        product_image = ProductImage.objects.create(path=storage_path, is_main=data["is_main"])
        product_image.save()

        product.product_images.add(product_image)

        return ProductImageSerializer(product_image)

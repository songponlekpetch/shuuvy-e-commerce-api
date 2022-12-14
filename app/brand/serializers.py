import uuid

from rest_framework import serializers
from core.serializers import BaseSerializer
from tag.serializers import TagSerializer
from core.models import Brand, Tag
from core.services.digitalocean_service import DigitalOceanService
from core.configs import BRANDS_FOLDER, DIGITAL_OCEAN_SETTINGS


class BrandSerializer(BaseSerializer):
    """Serializer for band"""
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta(BaseSerializer.Meta):
        model = Brand
        fields = BaseSerializer.Meta.fields + (
            "name",
            "description",
            "url",
            "facebook_contact",
            "instagram_contact",
            "line_contact",
            "image_path",
            "followers",
            "priority",
            "tags",
            "tag_ids",)
        read_only_fields = BaseSerializer.Meta.read_only_fields + (
            "image_path",
            "tags",)

    def _get_or_create_tags(self, tag_ids, brand):
        if tag_ids:
            for tag_id in tag_ids:
                tag = Tag.objects.get(id=tag_id)
                brand.tags.add(tag)

    def create(self, validated_data):
        """Create a new brand"""
        tag_ids = validated_data.pop("tag_ids", [])

        brand = Brand.objects.create(**validated_data)
        self._get_or_create_tags(tag_ids, brand)
        brand.save()

        return brand

    def update(self, pk, validated_data):
        """Update a brand"""
        brand = Brand.objects.get(pk=pk)
        tag_ids = validated_data.pop("tag_ids", [])
        brand = super().update(brand, validated_data)

        if tag_ids:
            self._get_or_create_tags(tag_ids, brand)

        brand.save()

        return brand


class UploadBrandSerializer(serializers.Serializer):
    image_file = serializers.ImageField()

    def create(self, brand):
        data = self.validated_data
        image_format = data["image_file"].name.split(".")[-1]

        if image_format not in ["jpg", "jpeg", "png"]:
            raise serializers.ValidationError(
                f"Invalid image format [{image_format}]")

        digital_ocean_service = DigitalOceanService(**DIGITAL_OCEAN_SETTINGS)
        storage_path = f"{BRANDS_FOLDER}/{brand.id}/{uuid.uuid4().hex}.{image_format}"
        image_path = digital_ocean_service.upload_file_to_storage(
            file=data["image_file"],
            storage_path=storage_path)

        brand.image_path = image_path
        brand.save()

        return BrandSerializer(brand)

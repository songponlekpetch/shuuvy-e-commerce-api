import uuid

from rest_framework import serializers

from core.serializers import BaseSerializer
from core.models import Category
from core.services.digitalocean_service import DigitalOceanService
from core.configs import DIGITAL_OCEAN_SETTINGS, CATEGORIES_FOLDER


class CategorySerializer(BaseSerializer):
    """Serializer for category"""

    class Meta(BaseSerializer.Meta):
        model = Category
        fields = BaseSerializer.Meta.fields + ("name", "image_path",)
        read_only_fields = BaseSerializer.Meta.read_only_fields + ("image_path",)


class UploadCategorySerializer(serializers.Serializer):
    image_file = serializers.ImageField()

    def create(self, category):
        data = self.validated_data
        image_format = data["image_file"].name.split(".")[-1]

        if image_format not in ["jpg", "jpeg", "png"]:
            raise serializers.ValidationError(
                f"Invalid image format [{image_format}]")

        digital_ocean_service = DigitalOceanService(**DIGITAL_OCEAN_SETTINGS)
        storage_path = f"{CATEGORIES_FOLDER}/{category.id}/{uuid.uuid4().hex}.{image_format}"
        storage_path = digital_ocean_service.upload_file_to_storage(file=data["image_file"], storage_path=storage_path)

        category.image_path = storage_path
        category.save()

        return CategorySerializer(category)

import uuid

from rest_framework import serializers

from core.serializers import BaseSerializer
from core.models import Subcategory
from category.serializers import CategorySerializer
from core.services.digitalocean_service import DigitalOceanService
from core.configs import SUBCATEGORIES_FOLDER, DIGITAL_OCEAN_SETTINGS


class SubcategorySerializer(BaseSerializer):
    """Serializer for subcategory"""
    category = CategorySerializer()

    class Meta(BaseSerializer.Meta):
        model = Subcategory
        fields = BaseSerializer.Meta.fields + ("name", "category", "image_path",)
        read_only_fields = BaseSerializer.Meta.read_only_fields + ("image_path",)


class UploadSubcategorySerializer(serializers.Serializer):
    image_file = serializers.ImageField()

    def create(self, subcategory):
        data = self.validated_data
        image_format = data["image_file"].name.split(".")[-1]

        if image_format not in ["jpg", "jpeg", "png"]:
            raise serializers.ValidationError(
                f"Invalid image format [{image_format}]")

        digital_ocean_service = DigitalOceanService(**DIGITAL_OCEAN_SETTINGS)
        storage_path = f"{SUBCATEGORIES_FOLDER}/{subcategory.id}/{uuid.uuid4().hex}.{image_format}"
        storage_path = digital_ocean_service.upload_file_to_storage(file=data["image_file"], storage_path=storage_path)

        subcategory.image_path = storage_path
        subcategory.save()

        return SubcategorySerializer(subcategory)

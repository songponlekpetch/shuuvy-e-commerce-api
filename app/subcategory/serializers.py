import uuid

from rest_framework import serializers

from core.serializers import BaseSerializer
from core.models import Subcategory
from category.serializers import CategorySerializer
from core.services.firebase_service import FirebaseService
from core.configs import FIREBASE_STORAGE_SUBCATEGORIES_FOLDER


class SubcategorySerializer(BaseSerializer):
    """Serializer for subcategory"""
    category = CategorySerializer()

    class Meta(BaseSerializer.Meta):
        model = Subcategory
        fields = BaseSerializer.Meta.fields + ("name", "category", "image_url",)
        read_only_fields = BaseSerializer.Meta.read_only_fields + ("image_url",)


class UploadSubcategorySerializer(serializers.Serializer):
    image_file = serializers.ImageField()

    def create(self, subcategory):
        data = self.validated_data
        image_format = data["image_file"].name.split(".")[-1]

        if image_format not in ["jpg", "jpeg", "png"]:
            raise serializers.ValidationError(
                f"Invalid image format [{image_format}]")

        firebase_service = FirebaseService()
        file_path = f"{FIREBASE_STORAGE_SUBCATEGORIES_FOLDER}/{subcategory.id}/{uuid.uuid4().hex}.{image_format}"
        image_url = firebase_service.upload_file_to_storage(file=data["image_file"], file_path=file_path)

        subcategory.image_url = image_url
        subcategory.save()

        return SubcategorySerializer(subcategory)
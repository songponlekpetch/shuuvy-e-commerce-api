import uuid

from rest_framework import serializers

from core.serializers import BaseSerializer
from core.models import Category
from core.services.firebase_service import FirebaseService
from core.configs import FIREBASE_STORAGE_CATEGORIES_FOLDER


class CategorySerializer(BaseSerializer):
    """Serializer for category"""

    class Meta(BaseSerializer.Meta):
        model = Category
        fields = BaseSerializer.Meta.fields + ("name", "image_url",)
        read_only_fields = BaseSerializer.Meta.read_only_fields + ("image_url",)


class UploadCategorySerializer(serializers.Serializer):
    image_file = serializers.ImageField()

    def create(self, category):
        data = self.validated_data
        image_format = data["image_file"].name.split(".")[-1]

        if image_format not in ["jpg", "jpeg", "png"]:
            raise serializers.ValidationError(
                f"Invalid image format [{image_format}]")

        firebase_service = FirebaseService()
        file_path = f"{FIREBASE_STORAGE_CATEGORIES_FOLDER}/{category.id}/{uuid.uuid4().hex}.{image_format}"
        image_url = firebase_service.upload_file_to_storage(file=data["image_file"], file_path=file_path)

        category.image_url = image_url
        category.save()

        return CategorySerializer(category)

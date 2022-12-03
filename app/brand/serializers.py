import uuid

from rest_framework import serializers
from core.serializers import BaseSerializer
from core.models import Brand
from core.services.firebase_service import FirebaseService
from core.configs import FIREBASE_STORAGE_BRANDS_FOLDER


class BrandSerializer(BaseSerializer):
    """Serializer for band"""

    class Meta(BaseSerializer.Meta):
        model = Brand
        fields = BaseSerializer.Meta.fields + (
            "name",
            "description",
            "url",
            "facebook_contact",
            "instagram_contact",
            "line_contact",
            "image_url",
            "followers",)
        read_only_fields = BaseSerializer.Meta.read_only_fields + ("image_url",)

class UploadBrandSerializer(serializers.Serializer):
    image_file = serializers.ImageField()

    def create(self, brand):
        data = self.validated_data
        image_format = data["image_file"].name.split(".")[-1]

        if image_format not in ["jpg", "jpeg", "png"]:
            raise serializers.ValidationError(
                f"Invalid image format [{image_format}]")

        firebase_service = FirebaseService()
        file_path = f"{FIREBASE_STORAGE_BRANDS_FOLDER}/{brand.id}/{uuid.uuid4().hex}.{image_format}"
        image_url = firebase_service.upload_file_to_storage(file=data["image_file"], file_path=file_path)

        brand.image_url = image_url
        brand.save()

        return BrandSerializer(brand)

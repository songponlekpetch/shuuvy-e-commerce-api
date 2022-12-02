from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    """Base serializer"""

    class Meta:
        fields = ("id", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
from core.serializers import BaseSerializer
from core.models import Category


class CategorySerializer(BaseSerializer):
    """Serializer for category"""

    class Meta(BaseSerializer.Meta):
        model = Category
        fields = BaseSerializer.Meta.fields + ("name",)

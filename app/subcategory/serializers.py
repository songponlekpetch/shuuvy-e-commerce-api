from drf_writable_nested import WritableNestedModelSerializer

from core.serializers import BaseSerializer
from core.models import Subcategory
from category.serializers import CategorySerializer


class SubcategorySerializer(BaseSerializer, WritableNestedModelSerializer):
    """Serializer for subcategory"""
    category = CategorySerializer()

    class Meta(BaseSerializer.Meta):
        model = Subcategory
        fields = BaseSerializer.Meta.fields + ("name", "category")

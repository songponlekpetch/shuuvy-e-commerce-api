from core.serializers import BaseSerializer
from core.models import Brand


class BrandSerializer(BaseSerializer):
    """Serializer for band"""

    class Meta(BaseSerializer.Meta):
        model = Brand
        fields = BaseSerializer.Meta.fields + ("name", "description", "url")

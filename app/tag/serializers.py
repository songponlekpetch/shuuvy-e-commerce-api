from core.serializers import BaseSerializer
from core.models import Tag


class TagSerializer(BaseSerializer):
    """Serializer for tag"""

    class Meta(BaseSerializer.Meta):
        model = Tag
        fields = BaseSerializer.Meta.fields + ("name",)

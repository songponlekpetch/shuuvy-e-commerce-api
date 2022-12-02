from core.serializers import BaseSerializer
from core.models import Promotion


class PromotionSerializer(BaseSerializer):
    """Serializer for promotion"""

    class Meta(BaseSerializer.Meta):
        model = Promotion
        fields = BaseSerializer.Meta.fields + (
            "discount_type",
            "discount",
            "expired_at",
            "is_active")

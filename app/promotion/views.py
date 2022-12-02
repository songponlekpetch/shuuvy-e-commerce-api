from rest_framework import viewsets

from core.models import Promotion
from promotion.serializers import PromotionSerializer


class PromotionViewSet(viewsets.ModelViewSet):
    serializer_class = PromotionSerializer
    queryset = Promotion.objects.all()
    http_method_names = ["get", "post", "delete", "put"]

    def get_queryset(self):
        return self.queryset.filter().order_by("-expired_at", "is_active")

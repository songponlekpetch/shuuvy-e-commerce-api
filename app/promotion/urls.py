from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter

from promotion import views

router = DefaultRouter()
router.register("", views.PromotionViewSet)

app_name = "promotion"

urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter

from brand import views

router = DefaultRouter()
router.register("", views.BrandViewSet)

app_name = "brand"

urlpatterns = [
    path("", include(router.urls)),
]

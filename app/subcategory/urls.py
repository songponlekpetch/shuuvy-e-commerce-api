from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter

from subcategory import views

router = DefaultRouter()
router.register("", views.SubcategoryViewSet)

app_name = "subcategory"

urlpatterns = [
    path("", include(router.urls)),
]

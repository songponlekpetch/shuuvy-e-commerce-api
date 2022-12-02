from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from product import views

router = SimpleRouter()
router.register("", views.ProductViewSet)

image_router = routers.NestedSimpleRouter(router, "", lookup="product")
image_router.register(
    "images",
    views.ProductImageViewSet,
    basename="product-images")

size_router = routers.NestedSimpleRouter(router, "", lookup="product")
size_router.register(
    "sizes",
    views.ProductSizeViewSet,
    basename="product-sizes")

color_router = routers.NestedSimpleRouter(router, "", lookup="product")
color_router.register(
    "colors",
    views.ProductColorViewSet,
    basename="product-colors")

model_router = routers.NestedSimpleRouter(router, "", lookup="product")
model_router.register(
    "models",
    views.ProductModelViewSet,
    basename="product-models")

app_name = "product"

urlpatterns = [
    path("", include(router.urls)),
    path("", include(image_router.urls)),
    path("", include(size_router.urls)),
    path("", include(color_router.urls)),
    path("", include(model_router.urls)),
]

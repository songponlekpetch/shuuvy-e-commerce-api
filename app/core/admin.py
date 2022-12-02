from django.contrib import admin

from core import models


class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "url")
    search_fields = ("id", "name", "url")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url", "status", "min_price", "max_price", "promotion")
    search_fields = ("id", "name", "url")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    search_fields = ("id", "name",)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    search_fields = ("id", "name", "category")


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    search_fields = ("id", "name",)

class PromotionAdmin(admin.ModelAdmin):
    list_display = ("id", "discount_type", "discount", "expired_at", "is_active")


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "path", "is_main")


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "product_image")


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product_color", "product_size", "price", "stock_quantity", "sale_quantity")
    search_fields = ("id", "name")


admin.site.register(models.User)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Subcategory, SubcategoryAdmin)
admin.site.register(models.Promotion, PromotionAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductSize, ProductSizeAdmin)
admin.site.register(models.ProductColor, ProductColorAdmin)
admin.site.register(models.ProductImage, ProductImageAdmin)
admin.site.register(models.ProductModel, ProductModelAdmin)

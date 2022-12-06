"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            val.replace(microsecond=0)
            print(val.isoformat())
            return val.isoformat()
        return ''


class UserManager(BaseUserManager):
    """Manager for user"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create, save and return a new superuser"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class BaseModel(models.Model):
    created_at = CustomDateTimeField(auto_now_add=True)
    updated_at = CustomDateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=255)
    image_path = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.name


class Subcategory(BaseModel):
    name = models.CharField(max_length=255)
    image_path = models.CharField(blank=True, max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DiscountType(models.TextChoices):
    AMOUNT = "amount"
    PERCENT = "percent"


class Promotion(BaseModel):
    discount_type = models.CharField(max_length=10, choices=DiscountType.choices, default=DiscountType.AMOUNT)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expired_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discount_type} - {self.discount}"


class ProductImage(BaseModel):
    path = models.CharField(max_length=255)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.path


class ProductColor(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    product_image = models.ForeignKey(ProductImage, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductSize(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductModel(BaseModel):
    name = models.CharField(max_length=255)
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    sale_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Brand(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    image_path = models.CharField(blank=True, null=True, default=None, max_length=255)
    facebook_contact = models.CharField(max_length=255, blank=True)
    instagram_contact = models.CharField(max_length=255, blank=True)
    line_contact = models.CharField(max_length=255, blank=True)
    followers = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name


class ProductStatus(models.TextChoices):
    HOT = "hot"
    SALE = "sale"
    NEW = "new"
    NORMAL = "normal"


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=255, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=ProductStatus.choices,
        default=ProductStatus.NORMAL)
    click_count = models.IntegerField(default=0)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    categories = models.ManyToManyField(Category, blank=True)
    subcategories = models.ManyToManyField(Subcategory, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    product_images = models.ManyToManyField(ProductImage, blank=True)
    product_colors = models.ManyToManyField(ProductColor, blank=True)
    product_sizes = models.ManyToManyField(ProductSize, blank=True)
    product_models = models.ManyToManyField(ProductModel, blank=True)

    def __str__(self):
        return self.name

# Generated by Django 4.1.3 on 2022-11-28 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_promotion_product_category_product_subcategory_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="category",
            new_name="categories",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="subcategory",
            new_name="subcategories",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="tag",
            new_name="tags",
        ),
    ]

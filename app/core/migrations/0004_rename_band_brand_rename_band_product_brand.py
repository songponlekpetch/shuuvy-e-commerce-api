# Generated by Django 4.1.3 on 2022-11-28 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_category_tag_subcategory"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Band",
            new_name="Brand",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="band",
            new_name="brand",
        ),
    ]

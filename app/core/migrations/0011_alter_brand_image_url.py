# Generated by Django 4.1.3 on 2022-12-03 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_alter_brand_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="image_url",
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]

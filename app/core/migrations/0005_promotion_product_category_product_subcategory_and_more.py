# Generated by Django 4.1.3 on 2022-11-28 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_rename_band_brand_rename_band_product_brand"),
    ]

    operations = [
        migrations.CreateModel(
            name="Promotion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "discount_type",
                    models.CharField(
                        choices=[("amount", "Amount"), ("percent", "Percent")], default="amount", max_length=10
                    ),
                ),
                ("discount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("expired_at", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ManyToManyField(blank=True, to="core.category"),
        ),
        migrations.AddField(
            model_name="product",
            name="subcategory",
            field=models.ManyToManyField(blank=True, to="core.subcategory"),
        ),
        migrations.AddField(
            model_name="product",
            name="tag",
            field=models.ManyToManyField(blank=True, to="core.tag"),
        ),
        migrations.AddField(
            model_name="product",
            name="promotion",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="core.promotion"
            ),
        ),
    ]

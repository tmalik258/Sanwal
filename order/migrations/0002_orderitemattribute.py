# Generated by Django 4.1.5 on 2023-08-11 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0012_alter_productspecification_options"),
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderItemAttribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.productspecificationvalue",
                    ),
                ),
                (
                    "order_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_item_attribute",
                        to="order.orderitem",
                    ),
                ),
            ],
        ),
    ]

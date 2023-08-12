# Generated by Django 4.1.5 on 2023-08-12 22:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("checkout", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="deliveryoptions",
            options={
                "ordering": ("order",),
                "verbose_name": "Delivery Option",
                "verbose_name_plural": "Delivery Options",
            },
        ),
        migrations.AlterField(
            model_name="deliveryoptions",
            name="order",
            field=models.IntegerField(
                default=0,
                help_text="Required - Order number of which it should be displayed in delivery option list on checkout page",
                verbose_name="Delivery Option Order Number",
            ),
        ),
    ]

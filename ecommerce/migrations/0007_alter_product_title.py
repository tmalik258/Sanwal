# Generated by Django 4.1.5 on 2023-05-09 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=124, unique=True),
        ),
    ]

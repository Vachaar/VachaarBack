# Generated by Django 5.1.4 on 2025-01-20 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]

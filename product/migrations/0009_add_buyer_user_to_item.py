# Generated by Django 5.1.4 on 2025-01-03 11:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_purchase_request_model'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='buyer_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bought_items', related_query_name='buyer', to=settings.AUTH_USER_MODEL, verbose_name='buyer user'),
        ),
    ]

# Generated by Django 5.1.4 on 2024-12-22 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='item_id',
            field=models.ForeignKey(help_text='The item linked to this banner (if any).', on_delete=django.db.models.deletion.CASCADE, to='product.item', verbose_name='Associated Item'),
        ),
    ]

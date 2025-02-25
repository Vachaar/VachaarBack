# Generated by Django 5.1.4 on 2025-01-03 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_banned',
            field=models.BooleanField(default=False, verbose_name='Is Banned'),
        ),
        migrations.AddField(
            model_name='item',
            name='state',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('sold', 'Sold'), ('reserved', 'Reserved')], default='active', max_length=20, verbose_name='State'),
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]

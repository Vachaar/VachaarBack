# Generated by Django 5.1.4 on 2024-12-21 04:46

import django.db.models.deletion
import reusable.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('title', models.CharField(help_text='The name of the category.', max_length=255, unique=True, verbose_name='Category Title')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='Item Title')),
                ('price', reusable.models.AmountField(decimal_places=18, max_digits=38, verbose_name='Price')),
                ('description', models.TextField(blank=True, verbose_name='Item Description')),
                ('transaction_status', models.CharField(choices=[('Active', 'Active'), ('Reserved', 'Reserved'), ('Sold', 'Sold'), ('Blocked', 'Blocked')], default='Active', max_length=10, verbose_name='Transaction Status')),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', related_query_name='category', to='product.category', verbose_name='Category')),
                ('reserver_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reserved_items', related_query_name='reserver', to=settings.AUTH_USER_MODEL, verbose_name='Reserver')),
                ('seller_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold_items', related_query_name='seller', to=settings.AUTH_USER_MODEL, verbose_name='Seller')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('order', models.PositiveSmallIntegerField(help_text='Determines the order in which banners are displayed. Lower values are shown first.', verbose_name='Display Order')),
                ('image_file', models.ImageField(help_text='The image file for the banner.', upload_to='banners/', verbose_name='Banner Image')),
                ('item_id', models.OneToOneField(blank=True, help_text='The item linked to this banner (if any).', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='banner', related_query_name='banner', to='product.item', verbose_name='Associated Item')),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
                'ordering': ['-order'],
            },
        ),
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('description', models.TextField(help_text='Details about the reported violation.', verbose_name='Violation Description')),
                ('status', models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Under Review', 'Under Review')], default='Under Review', help_text='The current status of the violation.', max_length=20, verbose_name='Violation Status')),
                ('item', models.ForeignKey(help_text='The item associated with this violation.', on_delete=django.db.models.deletion.CASCADE, related_name='violations', to='product.item', verbose_name='Reported Item')),
                ('reporter_user', models.ForeignKey(help_text='The user who reported this violation.', on_delete=django.db.models.deletion.CASCADE, related_name='reported_violations', to=settings.AUTH_USER_MODEL, verbose_name='Reporter User')),
            ],
            options={
                'verbose_name': 'Violation',
                'verbose_name_plural': 'Violations',
                'ordering': ['-id'],
            },
        ),
    ]
# Generated by Django 5.1.4 on 2024-12-31 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_managers_user_is_email_verified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sso_user_id',
            field=models.PositiveBigIntegerField(blank=True, db_index=True, null=True, unique=True),
        ),
    ]

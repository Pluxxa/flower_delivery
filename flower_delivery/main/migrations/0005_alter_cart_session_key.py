# Generated by Django 5.1.3 on 2024-11-09 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_cart_session_key_alter_cart_user_orderstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, unique=True),
        ),
    ]
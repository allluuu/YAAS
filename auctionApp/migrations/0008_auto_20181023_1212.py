# Generated by Django 2.1.2 on 2018-10-23 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctionApp', '0007_auto_20181023_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL),
        ),
    ]
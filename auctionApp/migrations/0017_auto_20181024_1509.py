# Generated by Django 2.1.2 on 2018-10-24 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionApp', '0016_auto_20181024_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=16),
        ),
    ]

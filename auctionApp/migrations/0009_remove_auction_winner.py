# Generated by Django 2.1.2 on 2018-10-23 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctionApp', '0008_auto_20181023_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='winner',
        ),
    ]

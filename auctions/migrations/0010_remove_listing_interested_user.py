# Generated by Django 4.2.1 on 2024-02-03 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='interested_user',
        ),
    ]

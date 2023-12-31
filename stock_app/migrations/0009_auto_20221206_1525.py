# Generated by Django 3.2.9 on 2022-12-06 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0008_auto_20221206_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='color',
        ),
        migrations.RemoveField(
            model_name='account',
            name='stock_ticker',
        ),
        migrations.AddField(
            model_name='account',
            name='stock',
            field=models.ManyToManyField(to='stock_app.Stock'),
        ),
        migrations.AddField(
            model_name='account',
            name='strategy',
            field=models.ManyToManyField(to='stock_app.Strategy'),
        ),
    ]

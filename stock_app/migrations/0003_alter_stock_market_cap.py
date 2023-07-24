# Generated by Django 4.1.3 on 2022-12-01 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0002_alter_stock_market_cap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='market_cap',
            field=models.DecimalField(decimal_places=30, default=100000000, max_digits=100),
        ),
    ]

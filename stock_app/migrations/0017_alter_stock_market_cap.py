# Generated by Django 3.2.9 on 2022-12-12 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0016_stock_market_cap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='market_cap',
            field=models.DecimalField(blank=True, decimal_places=30, default=100000000, max_digits=100, null=True),
        ),
    ]

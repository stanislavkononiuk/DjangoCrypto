# Generated by Django 4.1.3 on 2023-02-08 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0033_remove_strategy_stock_app_s_stock_i_f6525d_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='stock',
            name='stock_app_s_ticker_53c5e8_idx',
        ),
        migrations.RemoveIndex(
            model_name='strategy',
            name='stock_app_s_color_996f38_idx',
        ),
    ]

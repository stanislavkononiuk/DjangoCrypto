# Generated by Django 4.1.3 on 2023-02-01 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0032_alter_stock_high_alter_stock_low_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='strategy',
            name='stock_app_s_stock_i_f6525d_idx',
        ),
        migrations.AddIndex(
            model_name='strategy',
            index=models.Index(fields=['color'], name='stock_app_s_color_996f38_idx'),
        ),
    ]

# Generated by Django 3.2.9 on 2023-02-16 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0036_fedfundrate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fedfundrate',
            name='interest_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]

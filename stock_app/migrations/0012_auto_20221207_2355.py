# Generated by Django 3.2.9 on 2022-12-07 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0011_marketcap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='company_sector',
            field=models.CharField(blank=True, default='NOT PROVIDED', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='industry',
            field=models.CharField(blank=True, default='NOT PROVIDED', max_length=100, null=True),
        ),
    ]
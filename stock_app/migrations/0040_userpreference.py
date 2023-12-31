# Generated by Django 4.1.7 on 2023-03-31 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0039_smartmoney_remove_stock_stock_split_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('navbar_color', models.CharField(blank=True, max_length=100, null=True)),
                ('border_body', models.CharField(blank=True, max_length=100, null=True)),
                ('background_color', models.CharField(blank=True, max_length=100, null=True)),
                ('button_color', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]

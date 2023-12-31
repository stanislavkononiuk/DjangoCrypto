# Generated by Django 4.1.3 on 2022-12-01 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(blank=True, max_length=10, null=True)),
                ('exchange', models.CharField(blank=True, max_length=10, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('company_sector', models.CharField(blank=True, max_length=100, null=True)),
                ('industry', models.CharField(blank=True, max_length=100, null=True)),
                ('market_cap', models.DecimalField(blank=True, decimal_places=30, max_digits=100, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=30, max_digits=100, null=True)),
                ('volume', models.DecimalField(blank=True, decimal_places=30, max_digits=100, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=30, max_digits=100, null=True)),
                ('net_gain', models.DecimalField(blank=True, decimal_places=30, max_digits=100, null=True)),
                ('open', models.DecimalField(blank=True, decimal_places=30, max_digits=100, null=True)),
                ('low', models.DecimalField(blank=True, decimal_places=30, max_digits=100, null=True)),
                ('high', models.DecimalField(blank=True, decimal_places=30, max_digits=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('result', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('value', models.IntegerField(blank=True, default=100, null=True)),
                ('stock', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock_app.stock')),
            ],
        ),
        migrations.CreateModel(
            name='P',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('strategy', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='stock_app.strategy')),
            ],
        ),
    ]
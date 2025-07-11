# Generated by Django 5.1.4 on 2025-07-05 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_order_ghn_order_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province_code', models.CharField(blank=True, max_length=10, null=True)),
                ('province_name', models.CharField(blank=True, max_length=100, null=True)),
                ('district_code', models.CharField(blank=True, max_length=10, null=True)),
                ('district_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ward_code', models.CharField(blank=True, max_length=10, null=True)),
                ('ward_name', models.CharField(blank=True, max_length=100, null=True)),
                ('address_detail', models.CharField(blank=True, max_length=255, null=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address_detail', to='shop.order')),
            ],
        ),
    ]

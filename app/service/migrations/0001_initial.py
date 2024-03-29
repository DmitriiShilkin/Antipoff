# Generated by Django 5.0 on 2024-01-31 15:48

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('kadastr_number', models.CharField(max_length=254, unique=True, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Кадастровый номер')),
                ('latitude', models.FloatField(max_length=32, verbose_name='Широта')),
                ('longitude', models.FloatField(max_length=32, verbose_name='Долгота')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('message', models.CharField(max_length=254)),
                ('kadastr_number', models.CharField(blank=True, max_length=254, null=True)),
                ('latitude', models.FloatField(blank=True, max_length=32, null=True)),
                ('longitude', models.FloatField(blank=True, max_length=32, null=True)),
                ('query', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service.query')),
            ],
        ),
    ]

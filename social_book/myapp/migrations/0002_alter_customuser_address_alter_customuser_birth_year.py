# Generated by Django 5.1 on 2024-08-19 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=225),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='birth_year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

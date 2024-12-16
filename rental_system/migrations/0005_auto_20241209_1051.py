# Generated by Django 3.2.25 on 2024-12-09 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rental_system', '0004_auto_20241204_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenant',
            name='water_due',
        ),
        migrations.AddField(
            model_name='payment',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='property',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenants', to='rental_system.property'),
        ),
    ]

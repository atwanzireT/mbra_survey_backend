# Generated by Django 5.1.1 on 2025-04-03 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_concern_division'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concern',
            name='division',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='concern',
            name='road_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='concern',
            name='structure_photo',
            field=models.ImageField(blank=True, null=True, upload_to='structure_photos'),
        ),
        migrations.AlterField(
            model_name='concern',
            name='zone_or_village',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

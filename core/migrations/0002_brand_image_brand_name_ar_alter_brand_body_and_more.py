# Generated by Django 5.2.3 on 2025-06-22 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='brands', verbose_name='Brand Image'),
        ),
        migrations.AddField(
            model_name='brand',
            name='name_ar',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Brand Name (Arabic)'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='body',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Brand Name (English)'),
        ),
    ]

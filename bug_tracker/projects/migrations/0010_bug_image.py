# Generated by Django 4.0.2 on 2022-06-09 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_bug'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image'),
        ),
    ]
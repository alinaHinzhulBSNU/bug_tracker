# Generated by Django 4.0.2 on 2022-06-09 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_bug_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Image'),
        ),
    ]

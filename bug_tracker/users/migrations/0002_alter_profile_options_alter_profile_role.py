# Generated by Django 4.0.2 on 2022-06-03 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['role'], 'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('T', 'Tester'), ('D', 'Developer'), ('M', 'Manager')], max_length=2, verbose_name='Role'),
        ),
    ]
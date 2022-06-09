# Generated by Django 4.0.2 on 2022-06-09 14:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0008_alter_task_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2)], verbose_name='Text')),
                ('description', models.TextField(validators=[django.core.validators.MinLengthValidator(2)], verbose_name='Description')),
                ('reproducibility', models.CharField(choices=[('s', 'sometimes'), ('a', 'always')], max_length=2, verbose_name='Reproducibility')),
                ('severity', models.CharField(choices=[('1', 'minor'), ('2', 'medium'), ('3', 'major'), ('4', 'critical')], max_length=2, verbose_name='Severity')),
                ('priority', models.CharField(choices=[('a', 'ASAP'), ('h', 'high'), ('n', 'normal'), ('l', 'low')], max_length=2, verbose_name='Priority')),
                ('symptom', models.CharField(choices=[('cf', 'cosmetic flaw'), ('dl', 'data loss'), ('di', 'documentation issue'), ('io', 'incorrect operation'), ('ip', 'installation problem'), ('li', 'localization issue'), ('mf', 'missing feature'), ('s', 'scalability'), ('lp', 'low performance'), ('sc', 'system crash'), ('eb', 'unexpected behavior'), ('fb', 'unfriendly behavior'), ('vs', 'variance from specs '), ('e', 'enhancement')], max_length=3, verbose_name='Symptom')),
                ('workaround', models.BooleanField(default=False, verbose_name='Workaround')),
                ('start_time', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Start time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End time')),
                ('status', models.CharField(choices=[('0', 'backlog'), ('1', 'to do'), ('2', 'doing'), ('3', 'done')], max_length=2, verbose_name='Status')),
                ('performer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Performer')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Bug',
                'verbose_name_plural': 'Bugs',
                'ordering': ['start_time'],
            },
        ),
    ]

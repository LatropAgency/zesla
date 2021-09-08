# Generated by Django 3.2.7 on 2021-09-08 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0013_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'ACTUAL'), (2, 'VERSION'), (3, 'REQUEST')], default=1),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

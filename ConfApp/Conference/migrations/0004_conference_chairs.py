# Generated by Django 2.2.5 on 2019-12-30 01:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Conference', '0003_auto_20191230_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='chairs',
            field=models.ManyToManyField(related_name='chair_in', to=settings.AUTH_USER_MODEL),
        ),
    ]

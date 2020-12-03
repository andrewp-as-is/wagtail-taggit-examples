# -*- coding: utf-8 -*-
import django
from django.contrib.auth.models import User
from django.db import migrations

def create_superuser(apps, schema_editor):
    try:
        User.objects.create_superuser(username='admin', password='admin',email=None)
    except django.db.utils.IntegrityError:
        pass

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '__latest__'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]

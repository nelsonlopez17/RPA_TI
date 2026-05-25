# -*- coding: utf-8 -*-
from django.db import migrations, models
from django.conf import settings


def create_admins(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    admins = [
        {"username": "Nelson", "email": "Nelson@chardonaystore.com", "password": "chardonaystore123"},
        {"username": "Aronay", "email": "Aronay@chardonaystore.com", "password": "chardonaystore123"},
        {"username": "Yeidi", "email": "Yeidi@chardonaystore.com", "password": "chardonaystore123"},
    ]
    for admin in admins:
        if not User.objects.filter(username=admin["username"]).exists():
            user = User.objects.create_user(
                username=admin["username"],
                email=admin["email"],
                password=admin["password"],
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("ventas", "0002_factura_estado"),
    ]

    operations = [
        migrations.RunPython(create_admins, reverse_code=migrations.RunPython.noop),
    ]

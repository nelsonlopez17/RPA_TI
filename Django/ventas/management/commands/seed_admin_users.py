from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea usuarios administradores para Chardonay Store ERP'

    def handle(self, *args, **options):
        usuarios = [
            {
                'username': 'Aronay',
                'email': 'Aronay@chardonaystore.com',
                'password': 'chardonaystore123',
            },
            {
                'username': 'Nelson',
                'email': 'Nelson@chardonaystore.com',
                'password': 'chardonaystore123',
            },
            {
                'username': 'Yeidy',
                'email': 'Yeidy@chardonaystore.com',
                'password': 'chardonaystore123',
            },
        ]

        creados = 0
        existentes = 0

        for usuario_data in usuarios:
            username = usuario_data['username']
            email = usuario_data['email']
            password = usuario_data['password']

            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'WARN: Usuario "{username}" ya existe')
                )
                existentes += 1
            else:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f'OK: Usuario "{username}" creado')
                )
                creados += 1

        self.stdout.write(
            self.style.SUCCESS(f'\nResumen: {creados} creados, {existentes} ya existían')
        )

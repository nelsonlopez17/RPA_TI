from django.core.management.base import BaseCommand, CommandError
from decouple import config
from supabase import create_client, Client

# Usuarios a crear (username, email, password)
USERS = [
    {"username": "Nelson", "email": "Nelson@chardonaystore.com", "password": "chardonaystore123"},
    {"username": "Aronay", "email": "Aronay@chardonaystore.com", "password": "chardonaystore123"},
    {"username": "Yeidi", "email": "Yeidi@chardonaystore.com", "password": "chardonaystore123"},
]

class Command(BaseCommand):
    help = "Crea usuarios administradores directamente en Supabase usando el API admin."

    def handle(self, *args, **options):
        # Leer configuración de Supabase desde .env
        supabase_url = config('SUPABASE_URL', default='')
        supabase_key = config('SUPABASE_SERVICE_ROLE_KEY', default='')
        if not supabase_url or not supabase_key:
            raise CommandError('Variables SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY deben estar definidas en .env')

        # Inicializar cliente Supabase
        supabase: Client = create_client(supabase_url, supabase_key)

        created = 0
        existed = 0
        for user in USERS:
            try:
                # Intentar crear usuario via API admin
                resp = supabase.auth.admin.create_user(
                    email=user["email"],
                    password=user["password"],
                    email_confirm=True,
                    data={"username": user["username"]},
                )
                if resp.get('error'):
                    # Si el error indica que el usuario ya existe, lo contamos
                    if 'User already exists' in str(resp['error']):
                        self.stdout.write(self.style.WARNING(f'⚠️  Usuario "{user["username"]}" ya existe'))
                        existed += 1
                    else:
                        raise CommandError(f"Error creando {user['username']}: {resp['error']}")
                else:
                    self.stdout.write(self.style.SUCCESS(f'✅ Usuario "{user["username"]}" creado'))
                    created += 1
            except Exception as e:
                raise CommandError(f"Excepción al crear {user['username']}: {e}")

        self.stdout.write(self.style.SUCCESS(f"\n📊 Resumen: {created} creados, {existed} ya existían"))

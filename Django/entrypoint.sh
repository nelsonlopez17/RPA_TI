#!/bin/bash

# No esperar a PostgreSQL, solo ejecutar comandos
echo "🔄 Aplicando migraciones..."
python manage.py migrate --noinput --verbosity 2

echo "📦 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --verbosity 2

echo "✅ Iniciando gunicorn..."
exec "$@"

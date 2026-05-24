#!/bin/bash
set -e

echo "🔄 Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Iniciando aplicación Django..."
exec "$@"

#!/bin/bash

set -e

# Esperar a que la base de datos esté lista
echo "Esperando a que PostgreSQL esté listo..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER > /dev/null 2>&1; do
  sleep 1
done
echo "PostgreSQL está listo"

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Ejecutar comando pasado como argumento
echo "Iniciando aplicación..."
exec "$@"

#!/bin/bash
# Esperar a que PostgreSQL esté disponible
echo "Esperando a que PostgreSQL esté listo..."

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  echo "PostgreSQL no está disponible - esperando..."
  sleep 2
done

echo "¡PostgreSQL está listo!"

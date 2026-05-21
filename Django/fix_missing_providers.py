# fix_missing_providers.py
"""
Asignar automáticamente un proveedor predeterminado a los productos que no lo tengan.
Uso: python fix_missing_providers.py  (desde la raíz del proyecto Django)
"""
import os, sys

# Configurar Django
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion_base.settings')
sys.path.append(PROJECT_ROOT)
import django
django.setup()

from compras.models import Proveedor
from inventario.models import Producto

def main():
    default_supplier = Proveedor.objects.order_by('id').first()
    if not default_supplier:
        print('ERROR: No existing providers in the database.')
        return
    sin = Producto.objects.filter(proveedor_predeterminado__isnull=True)
    total = sin.count()
    if total == 0:
        print('All products already have a default provider.')
        return
    print(f'Found {total} product(s) missing a default provider.')
    sin.update(proveedor_predeterminado=default_supplier)
    print(f"Assigned provider '{default_supplier.nombre}' (id={default_supplier.id}) to {total} product(s).")

if __name__ == '__main__':
    main()

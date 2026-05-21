from django.db import migrations


def set_default_provider(apps, schema_editor):
    Producto = apps.get_model('inventario', 'Producto')
    Proveedor = apps.get_model('compras', 'Proveedor')
    # Ensure default provider exists
    default_provider, created = Proveedor.objects.get_or_create(nombre='Proveedor Predeterminado')
    # Update products with null provider_predeterminado
    Producto.objects.filter(proveedor_predeterminado__isnull=True).update(proveedor_predeterminado=default_provider)


def reverse_set_default_provider(apps, schema_editor):
    # No need to reverse the data change; keep existing providers.
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('inventario', '0004_alter_producto_proveedor_predeterminado'),
    ]

    operations = [
        migrations.RunPython(set_default_provider, reverse_set_default_provider),
    ]

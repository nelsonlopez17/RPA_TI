from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Producto, AlertaSistema

@receiver(post_save, sender=Producto)
def check_stock_level(sender, instance, **kwargs):
    if instance.stock < 10:
        proveedor_id = instance.proveedor_predeterminado.id if instance.proveedor_predeterminado else None
        proveedor_nombre = instance.proveedor_predeterminado.nombre if instance.proveedor_predeterminado else "Sin proveedor asignado"

        mensaje = (
            f"STOCK BAJO: {instance.nombre} (SKU: {instance.sku}) "
            f"tiene {instance.stock} unidades. "
            f"Proveedor: {proveedor_nombre}."
        )

        # Evitar alertas duplicadas no leidas para el mismo producto
        if not AlertaSistema.objects.filter(producto_id=instance.id, leida=False).exists():
            AlertaSistema.objects.create(
                tipo='Warning',
                mensaje=mensaje,
                producto_id=instance.id,
                proveedor_id=proveedor_id
            )

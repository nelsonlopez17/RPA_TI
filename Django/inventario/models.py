from django.db import models
from django.apps import apps

def get_default_provider():
    from compras.models import Proveedor
    provider, created = Proveedor.objects.get_or_create(nombre='Proveedor Predeterminado')
    return provider.id

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    proveedor_predeterminado = models.ForeignKey(
        'compras.Proveedor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=get_default_provider,
        related_name='productos',
        verbose_name='Proveedor Predeterminado'
    )

    def __str__(self):
        return f"[{self.sku}] {self.nombre}"

class AlertaSistema(models.Model):
    TIPO_CHOICES = [
        ('Info', 'Información'),
        ('Warning', 'Advertencia'),
        ('Critical', 'Crítico'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Info')
    mensaje = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    producto_id = models.IntegerField(null=True, blank=True)  # ID del producto que generó la alerta
    proveedor_id = models.IntegerField(null=True, blank=True)  # ID del proveedor sugerido

    def __str__(self):
        return f"[{self.tipo}] {self.mensaje}"

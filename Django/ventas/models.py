from django.db import models
from inventario.models import Producto

class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    nit = models.CharField(max_length=20, default='CF')
    correo = models.EmailField()
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    ESTADO_CHOICES = [
        ('Borrador', 'Borrador'),
        ('Emitida', 'Emitida'),
        ('Enviada', 'Enviada'),
        ('Pagada', 'Pagada'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=50, unique=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Emitida')

    def __str__(self):
        return f"Factura {self.numero_factura}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de Factura {self.factura.numero_factura} - {self.producto.nombre}"

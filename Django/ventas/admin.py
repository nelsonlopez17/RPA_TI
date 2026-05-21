from django.contrib import admin
from .models import Cliente, Factura, DetalleFactura

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'nit', 'correo', 'telefono')
    search_fields = ('nombre', 'nit')

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_factura', 'cliente', 'fecha_venta', 'total')
    list_filter = ('fecha_venta', 'cliente')
    search_fields = ('numero_factura',)

@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'factura', 'producto', 'cantidad', 'precio_unitario')

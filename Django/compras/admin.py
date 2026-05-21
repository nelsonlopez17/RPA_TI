from django.contrib import admin
from .models import Proveedor, OrdenCompra

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'contacto', 'telefono')
    search_fields = ('nombre',)

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'producto', 'cantidad', 'costo_total', 'fecha_compra')
    list_filter = ('proveedor', 'fecha_compra')

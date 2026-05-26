from rest_framework import serializers, viewsets
from .models import Factura, DetalleFactura

class DetalleFacturaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='factura.cliente.nombre', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetalleFactura
        fields = ['id', 'factura', 'producto', 'producto_nombre', 'cliente_nombre', 'cantidad', 'precio_unitario']

class DetalleFacturaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DetalleFactura.objects.select_related('factura__cliente', 'producto').all()
    serializer_class = DetalleFacturaSerializer

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

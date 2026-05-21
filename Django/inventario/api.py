from rest_framework import serializers, viewsets
from .models import Producto, AlertaSistema

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class AlertaSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertaSistema
        fields = '__all__'

class AlertaSistemaViewSet(viewsets.ModelViewSet):
    queryset = AlertaSistema.objects.all()
    serializer_class = AlertaSistemaSerializer

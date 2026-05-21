from django import forms
from django.forms import inlineformset_factory
from .models import Factura, DetalleFactura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente', 'numero_factura']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: F-00200'}),
        }

DetalleFacturaFormSet = inlineformset_factory(
    Factura,
    DetalleFactura,
    fields=['producto', 'cantidad'],
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True,
    widgets={
        'producto': forms.Select(attrs={'class': 'form-control detalle-producto'}),
        'cantidad': forms.NumberInput(attrs={'class': 'form-control detalle-cantidad', 'min': 1}),
    }
)

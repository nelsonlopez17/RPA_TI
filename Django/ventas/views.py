from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from configuracion_base.mixins import RoleRequiredMixin
from .models import Cliente, Factura, DetalleFactura
from .forms import FacturaForm, DetalleFacturaFormSet
from inventario.models import Producto

# --- Cliente Views ---
class ClienteListView(RoleRequiredMixin, ListView):
    allowed_roles = ['Administrador', 'Vendedor']
    model = Cliente
    template_name = 'ventas/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        qs = Cliente.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(nombre__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context

class ClienteCreateView(RoleRequiredMixin, View):
    allowed_roles = ['Administrador', 'Vendedor']
    template_name = 'ventas/cliente_form.html'

    def get(self, request):
        from django.forms import modelform_factory
        ClienteForm = modelform_factory(Cliente, fields=['nombre', 'nit', 'correo', 'telefono'])
        return render(request, self.template_name, {'form': ClienteForm()})

    def post(self, request):
        from django.forms import modelform_factory
        ClienteForm = modelform_factory(Cliente, fields=['nombre', 'nit', 'correo', 'telefono'])
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
        return render(request, self.template_name, {'form': form})

class ClienteUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador', 'Vendedor']
    model = Cliente
    template_name = 'ventas/cliente_form.html'
    fields = ['nombre', 'nit', 'correo', 'telefono']
    success_url = reverse_lazy('cliente_list')

class ClienteDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador', 'Vendedor']
    model = Cliente
    template_name = 'ventas/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')

# --- Factura Views ---
class FacturaListView(RoleRequiredMixin, ListView):
    allowed_roles = ['Administrador', 'Vendedor']
    model = Factura
    template_name = 'ventas/factura_list.html'
    context_object_name = 'facturas'
    paginate_by = 20

    def get_queryset(self):
        qs = Factura.objects.select_related('cliente').order_by('-fecha_venta')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(cliente__nombre__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class FacturaCreateView(RoleRequiredMixin, View):
    allowed_roles = ['Administrador', 'Vendedor']
    template_name = 'ventas/factura_form.html'

    def _get_productos(self):
        return list(Producto.objects.filter(stock__gt=0).values('id', 'nombre', 'precio_venta', 'stock'))

    def get(self, request):
        form = FacturaForm()
        formset = DetalleFacturaFormSet()
        return render(request, self.template_name, {
            'form': form, 'formset': formset,
            'productos': self._get_productos(), 'accion': 'Crear'
        })

    def post(self, request):
        form = FacturaForm(request.POST)
        formset = DetalleFacturaFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    factura = form.save(commit=False)
                    factura.total = Decimal('0.00')
                    factura.save()

                    total = Decimal('0.00')
                    detalles_validos = 0

                    for detalle_form in formset:
                        cd = detalle_form.cleaned_data
                        if cd and not cd.get('DELETE') and cd.get('producto'):
                            producto = cd['producto']
                            cantidad = cd['cantidad']

                            if cantidad > producto.stock:
                                messages.error(request, f'Stock insuficiente para "{producto.nombre}". Disponible: {producto.stock}')
                                factura.delete()
                                return render(request, self.template_name, {
                                    'form': form, 'formset': formset,
                                    'productos': self._get_productos(), 'accion': 'Crear'
                                })

                            DetalleFactura.objects.create(
                                factura=factura,
                                producto=producto,
                                cantidad=cantidad,
                                precio_unitario=producto.precio_venta
                            )
                            Producto.objects.filter(pk=producto.pk).update(stock=producto.stock - cantidad)
                            total += producto.precio_venta * cantidad
                            detalles_validos += 1

                    if detalles_validos == 0:
                        factura.delete()
                        messages.error(request, 'Debes agregar al menos un producto a la factura.')
                        return render(request, self.template_name, {
                            'form': form, 'formset': formset,
                            'productos': self._get_productos(), 'accion': 'Crear'
                        })

                    factura.total = total
                    factura.save()
                    messages.success(request, f'Factura {factura.numero_factura} creada. Total: Q. {total:,.2f}')
                    return redirect('factura_list')

            except Exception as e:
                messages.error(request, f'Error al guardar: {str(e)}')

        return render(request, self.template_name, {
            'form': form, 'formset': formset,
            'productos': self._get_productos(), 'accion': 'Crear'
        })


class FacturaDetailView(RoleRequiredMixin, View):
    allowed_roles = ['Administrador', 'Vendedor']
    template_name = 'ventas/factura_detail.html'

    def get(self, request, pk):
        factura = get_object_or_404(Factura.objects.select_related('cliente'), pk=pk)
        detalles = DetalleFactura.objects.filter(factura=factura).select_related('producto')
        return render(request, self.template_name, {
            'factura': factura,
            'detalles': detalles
        })

class FacturaUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador', 'Vendedor']
    model = Factura
    template_name = 'ventas/factura_form.html'
    fields = ['cliente', 'numero_factura', 'total']
    success_url = reverse_lazy('factura_list')

class FacturaDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador', 'Vendedor']
    model = Factura
    template_name = 'ventas/factura_confirm_delete.html'
    success_url = reverse_lazy('factura_list')

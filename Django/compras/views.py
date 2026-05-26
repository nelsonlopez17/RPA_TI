from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from configuracion_base.mixins import RoleRequiredMixin
from .models import Proveedor, OrdenCompra

# --- Proveedor Views ---
class ProveedorListView(RoleRequiredMixin, ListView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Proveedor
    template_name = 'compras/proveedor_list.html'
    context_object_name = 'proveedores'
    paginate_by = 20

    def get_queryset(self):
        from django.db.models import Q
        qs = Proveedor.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) |
                Q(contacto__icontains=q) |
                Q(telefono__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context

class ProveedorCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Proveedor
    template_name = 'compras/proveedor_form.html'
    fields = ['nombre', 'contacto', 'telefono']
    success_url = reverse_lazy('proveedor_list')

class ProveedorUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Proveedor
    template_name = 'compras/proveedor_form.html'
    fields = ['nombre', 'contacto', 'telefono']
    success_url = reverse_lazy('proveedor_list')

class ProveedorDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Proveedor
    template_name = 'compras/proveedor_confirm_delete.html'
    success_url = reverse_lazy('proveedor_list')

from django.views import View

# --- OrdenCompra Views ---
class OrdenCompraConfirmView(RoleRequiredMixin, View):
    allowed_roles = ['Administrador', 'Bodeguero']
    def post(self, request, *args, **kwargs):
        """Confirm the order: add product stock and update status."""
        from django.db.models import F
        from django.db import transaction
        with transaction.atomic():
            orden = OrdenCompra.objects.select_for_update().get(pk=kwargs['pk'])
            if orden.estado == 'Pendiente':
                producto = orden.producto
                producto.stock = F('stock') + orden.cantidad
                producto.save()
                orden.estado = 'Recibida'
                orden.save()
        return redirect('ordencompra_list')

class OrdenCompraListView(RoleRequiredMixin, ListView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = OrdenCompra
    template_name = 'compras/ordencompra_list.html'
    context_object_name = 'ordenes'
    paginate_by = 20

    def get_queryset(self):
        from django.db.models import Q
        qs = OrdenCompra.objects.select_related('proveedor', 'producto')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(proveedor__nombre__icontains=q) |
                Q(producto__nombre__icontains=q) |
                Q(estado__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context

class OrdenCompraCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = OrdenCompra
    template_name = 'compras/ordencompra_form.html'
    fields = ['proveedor', 'producto', 'cantidad', 'costo_total']
    success_url = reverse_lazy('ordencompra_list')

class OrdenCompraUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = OrdenCompra
    template_name = 'compras/ordencompra_form.html'
    fields = ['proveedor', 'producto', 'cantidad', 'costo_total']
    success_url = reverse_lazy('ordencompra_list')

from inventario.models import Producto

class OrdenCompraDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = OrdenCompra
    template_name = 'compras/ordencompra_confirm_delete.html'
    success_url = reverse_lazy('ordencompra_list')

    def delete(self, request, *args, **kwargs):
        """Update product stock before deleting the order only if it was received."""
        from django.db.models import F
        from django.db import transaction
        with transaction.atomic():
            orden = OrdenCompra.objects.select_for_update().get(pk=self.get_object().pk)
            if orden.estado == 'Recibida':
                producto = orden.producto
                producto.stock = F('stock') - orden.cantidad
                producto.save()
            orden.delete()
        return redirect('ordencompra_list')

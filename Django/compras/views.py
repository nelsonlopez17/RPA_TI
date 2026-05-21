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
        qs = Proveedor.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(nombre__icontains=q)
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
        """Confirm the order: add product stock and delete the order."""
        orden = OrdenCompra.objects.get(pk=kwargs['pk'])
        producto = orden.producto
        producto.stock = producto.stock + orden.cantidad
        producto.save()
        orden.delete()
        return redirect('ordencompra_list')

class OrdenCompraListView(RoleRequiredMixin, ListView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = OrdenCompra
    template_name = 'compras/ordencompra_list.html'
    context_object_name = 'ordenes'
    paginate_by = 20

    def get_queryset(self):
        qs = OrdenCompra.objects.select_related('proveedor', 'producto')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(proveedor__nombre__icontains=q)
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
        """Update product stock before deleting the order."""
        orden = self.get_object()
        producto = orden.producto
        producto.stock = producto.stock + orden.cantidad
        producto.save()
        return super().delete(request, *args, **kwargs)

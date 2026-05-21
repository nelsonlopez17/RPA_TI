from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from configuracion_base.mixins import RoleRequiredMixin
from .models import Producto, Proveedor

class ProductoDetailView(RoleRequiredMixin, DetailView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Producto
    template_name = 'inventario/producto_detail.html'
    context_object_name = 'producto'
    pk_url_kwarg = 'pk'

class ProductoChangeProviderView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Producto
    fields = ['proveedor_predeterminado']
    template_name = 'inventario/producto_change_provider.html'
    success_url = reverse_lazy('producto_list')
    pk_url_kwarg = 'pk'

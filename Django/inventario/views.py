from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from configuracion_base.mixins import RoleRequiredMixin
from .models import Categoria, Producto

# --- Categoria Views ---
class CategoriaListView(RoleRequiredMixin, ListView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Categoria
    template_name = 'inventario/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 20

    def get_queryset(self):
        qs = Categoria.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(nombre__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context

class CategoriaCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Categoria
    template_name = 'inventario/categoria_form.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('categoria_list')

class CategoriaUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Categoria
    template_name = 'inventario/categoria_form.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('categoria_list')

class CategoriaDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Categoria
    template_name = 'inventario/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria_list')

# --- Producto Views ---
class ProductoListView(RoleRequiredMixin, ListView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Producto
    template_name = 'inventario/producto_list.html'
    context_object_name = 'productos'
    paginate_by = 20

    def get_queryset(self):
        qs = Producto.objects.select_related('categoria')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(nombre__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context

class ProductoCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Producto
    template_name = 'inventario/producto_form.html'
    fields = ['nombre', 'sku', 'categoria', 'descripcion', 'precio_compra', 'precio_venta', 'stock', 'proveedor_predeterminado']
    success_url = reverse_lazy('producto_list')

class ProductoUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Producto
    template_name = 'inventario/producto_form.html'
    fields = ['nombre', 'sku', 'categoria', 'descripcion', 'precio_compra', 'precio_venta', 'stock', 'proveedor_predeterminado']
    success_url = reverse_lazy('producto_list')


class ProductoDetailView(RoleRequiredMixin, DetailView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Producto
    template_name = 'inventario/producto_detail.html'
    context_object_name = 'producto'

class ProductoDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Administrador', 'Bodeguero']
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')


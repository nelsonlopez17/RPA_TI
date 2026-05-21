from django.urls import path
from . import views

urlpatterns = [
    # Proveedores
    path('proveedores/', views.ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/nuevo/', views.ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedores/<int:pk>/editar/', views.ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('proveedores/<int:pk>/eliminar/', views.ProveedorDeleteView.as_view(), name='proveedor_delete'),
    
    # Órdenes de Compra
    path('ordenes/', views.OrdenCompraListView.as_view(), name='ordencompra_list'),
    path('ordenes/nueva/', views.OrdenCompraCreateView.as_view(), name='ordencompra_create'),
    path('ordenes/<int:pk>/editar/', views.OrdenCompraUpdateView.as_view(), name='ordencompra_update'),
    path('ordenes/<int:pk>/confirmar/', views.OrdenCompraConfirmView.as_view(), name='ordencompra_confirm'),
    path('ordenes/<int:pk>/eliminar/', views.OrdenCompraDeleteView.as_view(), name='ordencompra_delete'),
]

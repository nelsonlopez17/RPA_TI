"""
URL configuration for configuracion_base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import HomeView, ExportView

from rest_framework.routers import DefaultRouter
from inventario.api import ProductoViewSet, AlertaSistemaViewSet
from ventas.api import FacturaViewSet
from compras.api import OrdenCompraViewSet, ProveedorViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'alertas', AlertaSistemaViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'ordenes', OrdenCompraViewSet)
router.register(r'proveedores', ProveedorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('exportar/', ExportView.as_view(), name='exportacion'),
    path('inventario/', include('inventario.urls')),
    path('compras/', include('compras.urls')),
    path('ventas/', include('ventas.urls')),
    path('api/v1/', include(router.urls)),
    path('', include('django.contrib.auth.urls')),
]

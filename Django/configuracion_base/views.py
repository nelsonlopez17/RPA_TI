from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# ============================================================================
# HomeView - Dashboard Power BI (embebido via iframe)
# El dashboard anterior con Chart.js fue respaldado en templates/home_backup.html
# Para restaurarlo: renombrar home_backup.html → home.html y descomentar el
# get_context_data original en esta vista.
# ============================================================================

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    # El dashboard Power BI no requiere datos de contexto del servidor.
    # Todo se renderiza dentro del iframe directamente desde Power BI.
    #
    # --- CÓDIGO ORIGINAL (respaldo) ---
    # Si necesitas restaurar el dashboard anterior, descomenta lo siguiente
    # y cambia el template a 'home_backup.html':
    #
    # from inventario.models import Producto
    # from ventas.models import Cliente, Factura
    # from compras.models import OrdenCompra
    # from django.db.models import Sum, Count
    # from django.db.models.functions import TruncMonth
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['productos_count'] = Producto.objects.count()
    #     context['clientes_count'] = Cliente.objects.count()
    #     context['ordenes_pendientes'] = OrdenCompra.objects.filter(estado='Pendiente').count()
    #     total = Factura.objects.aggregate(Sum('total'))['total__sum']
    #     context['ventas_total'] = total if total else 0.0
    #     context['ventas_recientes'] = Factura.objects.select_related('cliente').order_by('-fecha_venta')[:5]
    #     context['bajo_stock'] = Producto.objects.filter(stock__lt=10).select_related('categoria').order_by('stock')[:5]
    #     ventas_mensuales = Factura.objects.annotate(
    #         month=TruncMonth('fecha_venta')
    #     ).values('month').annotate(total=Sum('total')).order_by('month')
    #     meses_nombres = {
    #         1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
    #         7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
    #     }
    #     chart_sales_labels = []
    #     chart_sales_values = []
    #     for vm in ventas_mensuales:
    #         if vm['month']:
    #             month_num = vm['month'].month
    #             chart_sales_labels.append(meses_nombres.get(month_num, str(month_num)))
    #             chart_sales_values.append(float(vm['total']))
    #     context['chart_sales_labels'] = chart_sales_labels
    #     context['chart_sales_values'] = chart_sales_values
    #     from inventario.models import Categoria
    #     cats = Categoria.objects.annotate(num_productos=Count('producto')).values('nombre', 'num_productos')
    #     context['chart_cat_labels'] = [c['nombre'] for c in cats]
    #     context['chart_cat_values'] = [c['num_productos'] for c in cats]
    #     return context

import csv
import io
import zipfile
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from configuracion_base.mixins import RoleRequiredMixin
from inventario.models import Categoria, Producto
from ventas.models import DetalleFactura, Cliente, Factura
from compras.models import Proveedor, OrdenCompra

class ExportView(RoleRequiredMixin, View):
    allowed_roles = ['Administrador'] # Restringir a administradores
    template_name = 'exportacion.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        tipo_exportacion = request.POST.get('tipo_exportacion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Helper para generar CSV en memoria
        def generar_csv(headers, data_func, queryset):
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(headers)
            for obj in queryset:
                writer.writerow(data_func(obj))
            return output.getvalue()

        # Diccionario con todos los exportadores disponibles
        exportadores = {
            'clientes': {
                'headers': ['id', 'nombre', 'nit', 'correo', 'telefono'],
                'data': lambda c: [c.id, c.nombre, c.nit, c.correo, c.telefono],
                'qs': Cliente.objects.all()
            },
            'proveedores': {
                'headers': ['id', 'nombre', 'contacto', 'telefono', 'email'],
                'data': lambda p: [p.id, p.nombre, p.contacto, p.telefono, p.email or ''],
                'qs': Proveedor.objects.all()
            },
            'categorias': {
                'headers': ['id', 'nombre', 'descripcion'],
                'data': lambda c: [c.id, c.nombre, c.descripcion],
                'qs': Categoria.objects.all()
            },
            'productos': {
                'headers': ['id', 'sku', 'nombre', 'descripcion', 'precio_compra', 'precio_venta', 'stock', 'categoria', 'proveedor_predeterminado'],
                'data': lambda p: [p.id, p.sku, p.nombre, p.descripcion, p.precio_compra, p.precio_venta, p.stock, p.categoria.nombre if p.categoria else '', p.proveedor_predeterminado.nombre if p.proveedor_predeterminado else ''],
                'qs': Producto.objects.select_related('categoria', 'proveedor_predeterminado').all()
            },
            'facturas': {
                'headers': ['id', 'numero_factura', 'fecha_venta', 'cliente', 'total'],
                'data': lambda f: [f.id, f.numero_factura, f.fecha_venta.strftime('%Y-%m-%d %H:%M:%S') if f.fecha_venta else '', f.cliente.nombre if f.cliente else '', f.total],
                'qs': Factura.objects.select_related('cliente').all()
            },
            'detalle_facturas': {
                'headers': ['id', 'factura_id', 'producto', 'cantidad', 'precio_unitario', 'subtotal'],
                'data': lambda d: [d.id, d.factura.id, d.producto.nombre, d.cantidad, d.precio_unitario, d.cantidad * d.precio_unitario],
                'qs': DetalleFactura.objects.select_related('factura', 'producto').all()
            },
            'ordenes_compra': {
                'headers': ['id', 'proveedor', 'producto', 'cantidad', 'costo_total', 'fecha_compra'],
                'data': lambda o: [o.id, o.proveedor.nombre, o.producto.nombre, o.cantidad, o.costo_total, o.fecha_compra.strftime('%Y-%m-%d %H:%M:%S') if o.fecha_compra else ''],
                'qs': OrdenCompra.objects.select_related('proveedor', 'producto').all()
            }
        }

        # Aplicar filtros si existen
        if fecha_inicio:
            try:
                dt_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                exportadores['facturas']['qs'] = exportadores['facturas']['qs'].filter(fecha_venta__gte=dt_inicio)
                exportadores['ordenes_compra']['qs'] = exportadores['ordenes_compra']['qs'].filter(fecha_compra__gte=dt_inicio)
            except ValueError:
                pass

        if fecha_fin:
            try:
                # Se ajusta al final del día
                dt_fin = datetime.strptime(f"{fecha_fin} 23:59:59", '%Y-%m-%d %H:%M:%S')
                exportadores['facturas']['qs'] = exportadores['facturas']['qs'].filter(fecha_venta__lte=dt_fin)
                exportadores['ordenes_compra']['qs'] = exportadores['ordenes_compra']['qs'].filter(fecha_compra__lte=dt_fin)
            except ValueError:
                pass

        if tipo_exportacion == 'todo':
            # Generar ZIP con todos los archivos
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for nombre, exp in exportadores.items():
                    csv_data = generar_csv(exp['headers'], exp['data'], exp['qs'])
                    zip_file.writestr(f"{nombre}.csv", csv_data)
            
            response = HttpResponse(buffer.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="erp_export_completo_{datetime.now().strftime("%Y%m%d_%H%M")}.zip"'
            return response

        elif tipo_exportacion in exportadores:
            # Exportar un solo archivo
            exp = exportadores[tipo_exportacion]
            csv_data = generar_csv(exp['headers'], exp['data'], exp['qs'])
            
            response = HttpResponse(csv_data, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{tipo_exportacion}_{datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
            return response
        
        else:
            messages.error(request, 'Opción de exportación inválida.')
            return redirect('exportacion')

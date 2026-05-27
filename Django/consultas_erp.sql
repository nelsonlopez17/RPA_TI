-- ============================================================================
-- CONSULTAS SQL PARA ERP - SISTEMA DE GESTIÓN INTEGRAL
-- Base de datos: PostgreSQL
-- ============================================================================
-- 
-- TABLAS DEL SISTEMA (nombres generados por Django):
--   compras_proveedor        -> Proveedores
--   compras_ordencompra      -> Órdenes de compra
--   inventario_categoria     -> Categorías de productos
--   inventario_producto      -> Productos
--   inventario_alertasistema -> Alertas del sistema
--   ventas_cliente           -> Clientes
--   ventas_factura           -> Facturas de venta
--   ventas_detallefactura    -> Detalle de cada factura (líneas de venta)
-- ============================================================================


-- ============================================================================
-- 1. CONSULTAR TODAS LAS TABLAS DEL SISTEMA
-- ============================================================================
-- Esta consulta lista todas las tablas existentes en el schema 'public' de
-- PostgreSQL, filtrando únicamente las tablas de la aplicación (prefijos:
-- compras_, inventario_, ventas_) y excluyendo las tablas internas de Django
-- como auth_*, django_*, etc.
-- ============================================================================

SELECT 
    table_name                          AS tabla,
    pg_size_pretty(
        pg_total_relation_size(
            quote_ident(table_name)
        )
    )                                   AS tamaño,
    (SELECT COUNT(*) 
     FROM information_schema.columns c 
     WHERE c.table_name = t.table_name 
       AND c.table_schema = 'public')   AS num_columnas
FROM information_schema.tables t
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
  AND (
        table_name LIKE 'compras_%'
     OR table_name LIKE 'inventario_%'
     OR table_name LIKE 'ventas_%'
  )
ORDER BY table_name;


-- ============================================================================
-- 2. VENTAS POR PERIODO
-- ============================================================================
-- Resumen de ventas agrupadas por mes y año. Muestra la cantidad de facturas
-- emitidas, el total facturado y el promedio por factura en cada periodo.
-- Se pueden ajustar las fechas en la cláusula WHERE para filtrar un rango
-- específico. Solo se consideran facturas en estado 'Emitida' (activas).
-- ============================================================================

-- 2a. Ventas agrupadas por MES
SELECT 
    TO_CHAR(f.fecha_venta, 'YYYY-MM')               AS periodo,
    TO_CHAR(f.fecha_venta, 'TMMonth YYYY')           AS mes_nombre,
    COUNT(f.id)                                       AS total_facturas,
    COALESCE(SUM(f.total), 0)                         AS total_facturado,
    COALESCE(ROUND(AVG(f.total), 2), 0)               AS promedio_por_factura,
    COUNT(DISTINCT f.cliente_id)                       AS clientes_unicos
FROM ventas_factura f
WHERE f.estado = 'Emitida'
  -- Ajustar el rango de fechas según necesidad:
  -- AND f.fecha_venta BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY 
    TO_CHAR(f.fecha_venta, 'YYYY-MM'),
    TO_CHAR(f.fecha_venta, 'TMMonth YYYY')
ORDER BY periodo DESC;


-- 2b. Ventas agrupadas por DÍA (útil para análisis detallado)
SELECT 
    DATE(f.fecha_venta)                               AS fecha,
    COUNT(f.id)                                       AS total_facturas,
    COALESCE(SUM(f.total), 0)                         AS total_facturado,
    COUNT(DISTINCT f.cliente_id)                       AS clientes_unicos
FROM ventas_factura f
WHERE f.estado = 'Emitida'
  -- Ajustar el rango de fechas según necesidad:
  -- AND f.fecha_venta BETWEEN '2025-06-01' AND '2025-06-30'
GROUP BY DATE(f.fecha_venta)
ORDER BY fecha DESC;


-- ============================================================================
-- 3. PRODUCTOS MÁS VENDIDOS
-- ============================================================================
-- Ranking de los 20 productos con mayor volumen de ventas. Se calcula la
-- cantidad total vendida, el ingreso generado, el número de facturas donde
-- aparece cada producto y el precio promedio al que se vendió. Se une con
-- la tabla de categorías para dar contexto adicional.
-- ============================================================================

SELECT 
    p.id                                              AS producto_id,
    p.sku                                             AS sku,
    p.nombre                                          AS producto,
    cat.nombre                                        AS categoria,
    SUM(df.cantidad)                                  AS total_unidades_vendidas,
    SUM(df.cantidad * df.precio_unitario)             AS ingreso_total,
    COUNT(DISTINCT df.factura_id)                     AS num_facturas,
    ROUND(AVG(df.precio_unitario), 2)                 AS precio_promedio_venta,
    p.precio_venta                                    AS precio_lista_actual,
    p.stock                                           AS stock_actual
FROM ventas_detallefactura df
INNER JOIN inventario_producto p   ON df.producto_id = p.id
LEFT  JOIN inventario_categoria cat ON p.categoria_id = cat.id
INNER JOIN ventas_factura f        ON df.factura_id = f.id
WHERE f.estado = 'Emitida'
GROUP BY p.id, p.sku, p.nombre, cat.nombre, p.precio_venta, p.stock
ORDER BY total_unidades_vendidas DESC
LIMIT 20;


-- ============================================================================
-- 4. CLIENTES PRINCIPALES
-- ============================================================================
-- Ranking de los 20 clientes con mayor volumen de compras. Se muestra el total
-- gastado, número de facturas, promedio por factura, la fecha de su primera y
-- última compra para medir antigüedad y actividad reciente. Útil para
-- identificar clientes VIP y estrategias de fidelización.
-- ============================================================================

SELECT 
    c.id                                              AS cliente_id,
    c.nombre                                          AS cliente,
    c.nit                                             AS nit,
    c.correo                                          AS correo,
    c.telefono                                        AS telefono,
    COUNT(f.id)                                       AS total_facturas,
    COALESCE(SUM(f.total), 0)                         AS total_comprado,
    COALESCE(ROUND(AVG(f.total), 2), 0)               AS promedio_por_factura,
    MIN(f.fecha_venta)                                AS primera_compra,
    MAX(f.fecha_venta)                                AS ultima_compra,
    -- Días desde la última compra (para medir actividad reciente)
    EXTRACT(DAY FROM NOW() - MAX(f.fecha_venta))      AS dias_sin_comprar
FROM ventas_cliente c
LEFT JOIN ventas_factura f ON f.cliente_id = c.id AND f.estado = 'Emitida'
GROUP BY c.id, c.nombre, c.nit, c.correo, c.telefono
ORDER BY total_comprado DESC
LIMIT 20;


-- ============================================================================
-- 5. INVENTARIO DISPONIBLE
-- ============================================================================
-- Vista completa del inventario actual. Muestra cada producto con su stock,
-- precios de compra y venta, margen de ganancia (en monto y porcentaje),
-- valor total del inventario a precio de costo y a precio de venta,
-- categoría y proveedor predeterminado. Incluye un resumen totalizador
-- al final.
-- ============================================================================

-- 5a. Detalle de inventario por producto
SELECT 
    p.id                                              AS producto_id,
    p.sku                                             AS sku,
    p.nombre                                          AS producto,
    cat.nombre                                        AS categoria,
    prov.nombre                                       AS proveedor,
    p.stock                                           AS stock_actual,
    p.precio_compra                                   AS precio_compra,
    p.precio_venta                                    AS precio_venta,
    (p.precio_venta - p.precio_compra)                AS margen_unitario,
    CASE 
        WHEN p.precio_compra > 0 
        THEN ROUND(
            ((p.precio_venta - p.precio_compra) / p.precio_compra) * 100, 2
        )
        ELSE 0 
    END                                               AS margen_porcentaje,
    (p.stock * p.precio_compra)                       AS valor_inventario_costo,
    (p.stock * p.precio_venta)                        AS valor_inventario_venta,
    CASE 
        WHEN p.stock = 0  THEN ' SIN STOCK'
        WHEN p.stock < 5  THEN '  STOCK BAJO'
        WHEN p.stock < 20 THEN ' STOCK MEDIO'
        ELSE ' STOCK OK'
    END                                               AS estado_stock
FROM inventario_producto p
LEFT JOIN inventario_categoria cat  ON p.categoria_id = cat.id
LEFT JOIN compras_proveedor prov    ON p.proveedor_predeterminado_id = prov.id
ORDER BY cat.nombre, p.nombre;


-- 5b. Resumen total del inventario (una sola fila con totales globales)
SELECT 
    COUNT(*)                                          AS total_productos,
    SUM(p.stock)                                      AS total_unidades,
    SUM(p.stock * p.precio_compra)                    AS valor_total_costo,
    SUM(p.stock * p.precio_venta)                     AS valor_total_venta,
    SUM(p.stock * p.precio_venta) 
        - SUM(p.stock * p.precio_compra)              AS ganancia_potencial,
    COUNT(*) FILTER (WHERE p.stock = 0)               AS productos_sin_stock,
    COUNT(*) FILTER (WHERE p.stock > 0 AND p.stock < 5) AS productos_stock_bajo,
    ROUND(AVG(p.stock), 1)                            AS stock_promedio
FROM inventario_producto p;


-- ============================================================================
-- 6. PRODUCTOS CON STOCK POR DEBAJO DE 10 UNIDADES
-- ============================================================================
-- Alerta de productos con inventario crítico (menos de 10 unidades disponibles).
-- Incluye información del proveedor predeterminado para facilitar el proceso
-- de reorden. También muestra el histórico de ventas recientes (últimos 30 días)
-- para priorizar la reposición según demanda. Los productos con stock = 0
-- aparecen primero.
-- ============================================================================

SELECT 
    p.id                                              AS producto_id,
    p.sku                                             AS sku,
    p.nombre                                          AS producto,
    cat.nombre                                        AS categoria,
    p.stock                                           AS stock_actual,
    p.precio_compra                                   AS precio_compra,
    prov.nombre                                       AS proveedor,
    prov.telefono                                     AS telefono_proveedor,
    prov.email                                        AS email_proveedor,
    -- Unidades vendidas en los últimos 30 días (para estimar urgencia)
    COALESCE(
        (SELECT SUM(df.cantidad) 
         FROM ventas_detallefactura df
         INNER JOIN ventas_factura f ON df.factura_id = f.id
         WHERE df.producto_id = p.id 
           AND f.estado = 'Emitida'
           AND f.fecha_venta >= NOW() - INTERVAL '30 days'),
        0
    )                                                 AS vendidos_ultimos_30_dias,
    -- Última orden de compra para este producto
    (SELECT MAX(oc.fecha_compra) 
     FROM compras_ordencompra oc 
     WHERE oc.producto_id = p.id)                     AS ultima_orden_compra,
    -- Estado de urgencia
    CASE 
        WHEN p.stock = 0 THEN ' AGOTADO - REORDEN URGENTE'
        WHEN p.stock <= 10 THEN ' CRÍTICO - REORDENAR YA'
        ELSE ' BAJO - PLANIFICAR REORDEN'
    END                                               AS nivel_urgencia
FROM inventario_producto p
LEFT JOIN inventario_categoria cat  ON p.categoria_id = cat.id
LEFT JOIN compras_proveedor prov    ON p.proveedor_predeterminado_id = prov.id
WHERE p.stock < 10
ORDER BY p.stock ASC, vendidos_ultimos_30_dias DESC;


-- ============================================================================
-- FIN DEL ARCHIVO DE CONSULTAS
-- ============================================================================

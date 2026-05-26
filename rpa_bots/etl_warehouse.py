import requests
import pandas as pd
import os
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')

API_BASE = "https://erp-django-smea.onrender.com/api/v1"
DW_DIR = "data_warehouse"

def get_data(endpoint):
    response = requests.get(f"{API_BASE}/{endpoint}/")
    if response.status_code == 200:
        data = response.json()
        return data if isinstance(data, list) else data.get('results', [])
    return []

def run_etl():
    print("🚀 Iniciando Proceso ETL (Data Warehouse)...")
    
    if not os.path.exists(DW_DIR):
        os.makedirs(DW_DIR)
        
    print("📥 Extrayendo datos desde el ERP...")
    facturas = get_data("facturas")
    productos = get_data("productos")
    
    if not facturas or not productos:
        print("❌ Faltan datos para realizar el ETL.")
        return
        
    df_facturas = pd.DataFrame(facturas)
    df_productos = pd.DataFrame(productos)
    
    print("⚙️ Transformando Dimensiones (Dim_Producto)...")
    # Limpiar columnas innecesarias
    dim_producto = df_productos[['id', 'sku', 'nombre', 'categoria']]
    dim_producto.to_csv(f"{DW_DIR}/Dim_Producto.csv", index=False)
    
    print("⚙️ Transformando Dimensiones (Dim_Tiempo)...")
    # Extraer fechas únicas de ventas
    df_facturas['fecha_venta'] = pd.to_datetime(df_facturas['fecha_venta'], utc=True, format='ISO8601')
    fechas = df_facturas['fecha_venta'].dt.date.unique()
    dim_tiempo = pd.DataFrame({'fecha_id': fechas})
    dim_tiempo['fecha_id'] = pd.to_datetime(dim_tiempo['fecha_id'])
    dim_tiempo['año'] = dim_tiempo['fecha_id'].dt.year
    dim_tiempo['mes'] = dim_tiempo['fecha_id'].dt.month
    dim_tiempo['trimestre'] = dim_tiempo['fecha_id'].dt.quarter
    dim_tiempo.to_csv(f"{DW_DIR}/Dim_Tiempo.csv", index=False)
    
    print("⚙️ Construyendo Hechos (Fact_Ventas)...")
    # Crear Fact Table conectando IDs
    # (En un escenario real cruzaríamos Detalles de Factura para tener cantidades por producto)
    fact_ventas = df_facturas[['id', 'numero_factura', 'cliente', 'total', 'fecha_venta']].copy()
    fact_ventas['fecha_id'] = fact_ventas['fecha_venta'].dt.date
    fact_ventas = fact_ventas.drop(columns=['fecha_venta'])
    fact_ventas.to_csv(f"{DW_DIR}/Fact_Ventas.csv", index=False)
    
    print(f"✅ Proceso ETL completado. Data Warehouse generado en la carpeta '{DW_DIR}/'")
    print("📊 ¡Archivos CSV listos para importar a Power BI con esquema de estrella!")

if __name__ == "__main__":
    run_etl()

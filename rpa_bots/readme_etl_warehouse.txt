=========================================
ETL PARA DATA WAREHOUSE (POWER BI)
=========================================

Archivo: etl_warehouse.py

DESCRIPCION:
A diferencia de los otros bots (RPA) que realizan tareas transaccionales (comprar, facturar), este es un bot analitico (Inteligencia de Negocios). Su trabajo es Extraer, Transformar y Cargar (ETL) la informacion del ERP hacia un Data Warehouse optimizado.

COMO FUNCIONA:
1. Extrae: Utiliza la API del ERP para recolectar TODA la data cruda de Facturas y Productos.
2. Transforma: Utiliza la libreria 'pandas' (DataFrames) para manipular la data en memoria. Por ejemplo, rompe las fechas de venta en columnas de 'Ano', 'Mes' y 'Trimestre'.
3. Carga: Construye un modelo analitico conocido como "Esquema de Estrella".
4. Exporta los resultados en archivos CSV ultra-limpios dentro de la carpeta /data_warehouse/.

INSTRUCCIONES DE USO:
1. Asegurate de tener instalada la libreria pandas (pip install pandas).
2. Asegurate de que el servidor Django del ERP este corriendo.
3. Abre tu terminal en esta carpeta y ejecuta:
   python etl_warehouse.py
4. Conecta tu Power BI directamente a los archivos CSV que se generaran en la carpeta /data_warehouse/.

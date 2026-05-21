=========================================
BOT DE DATA ENTRY (REGISTRO MASIVO)
=========================================

Archivo: data_entry_bot.py

DESCRIPCION:
Este bot simula a un operador humano registrando grandes volumenes de inventario en el ERP. Su proposito es ahorrar horas de trabajo manual al insertar informacion directamente en el sistema de forma automatizada y estructurada.

COMO FUNCIONA:
1. Lee el archivo local 'data/nuevos_productos.csv' donde estan listados los productos enviados por el proveedor.
2. Itera linea por linea sobre el archivo (extrayendo SKU, nombre, precios, etc.).
3. Se conecta de forma ultra-rapida a la API del ERP (http://127.0.0.1:8000/api/v1/productos/).
4. Ejecuta un POST request inyectando el producto en la base de datos central.

INSTRUCCIONES DE USO:
1. Asegurate de que el servidor Django del ERP este corriendo.
2. Si tienes nuevos productos, agregalos al archivo 'data/nuevos_productos.csv'.
3. Abre tu terminal en esta carpeta y ejecuta:
   python data_entry_bot.py

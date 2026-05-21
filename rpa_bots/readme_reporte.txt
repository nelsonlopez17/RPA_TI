=========================================
BOT DE FACTURACION Y REPORTES
=========================================

Archivo: reporte_bot.py

DESCRIPCION:
Este bot de notificacion y reportes escanea continuamente el ERP en busca de facturas recien generadas para "enviarlas" a los clientes. Es un ejemplo perfecto de RPA de mensajeria y seguimiento de estados.

COMO FUNCIONA:
1. Contacta a la API del ERP consultando el endpoint de Facturas (http://127.0.0.1:8000/api/v1/facturas/).
2. Filtra la informacion buscando unicamente las facturas que tengan el estado 'Emitida' (lo que indica que el vendedor ya la creo pero aun no se entrega).
3. Simula el tiempo de ensamblaje de un archivo PDF o cruce de datos.
4. "Envia" la notificacion al cliente (simulado en consola).
5. Hace una peticion PATCH a la API del ERP para cambiar el estado de la factura de 'Emitida' a 'Enviada', evitando re-procesar facturas en el futuro.

INSTRUCCIONES DE USO:
1. Crea una factura nueva en tu ERP (desde la interfaz grafica de Ventas).
2. Abre tu terminal en esta carpeta y ejecuta:
   python reporte_bot.py
3. Observa como el bot encuentra tu factura y cambia su estado internamente.

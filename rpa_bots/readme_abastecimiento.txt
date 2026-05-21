=========================================
BOT DE ABASTECIMIENTO M2M (Machine-to-Machine)
=========================================

Archivo: abastecimiento_bot.py

DESCRIPCION:
Este bot es el mas complejo operativamente. Muestra como dos partes del sistema pueden actuar de forma autonoma sin requerir intervencion humana. Monitorea alertas criticas del ERP y genera transacciones financieras reales para solucionar problemas.

COMO FUNCIONA:
1. Revisa constantemente el panel de Alertas del ERP mediante la API.
2. Si detecta una alerta de Bajo Stock (Warning) que el sistema marco como no leida (leida=False), inicia el protocolo de abastecimiento.
3. Se conecta al modulo de Compras via API (http://127.0.0.1:8000/api/v1/ordenes/).
4. Crea automaticamente una nueva Orden de Compra para solicitar mas inventario al proveedor.
5. Vuelve al modulo de alertas y marca la alerta especifica como 'leida=True' (limpiando asi la bandeja de entrada y dando el incidente por resuelto).

INSTRUCCIONES DE USO:
1. En tu ERP, entra a facturacion y vende muchas unidades de un producto hasta que su Stock quede por debajo de 10.
2. Esto hara que el ERP (usando Signals) genere una alerta invisible.
3. Abre tu terminal en esta carpeta y ejecuta:
   python abastecimiento_bot.py
4. El bot comprara inventario por ti. Entra al ERP a la seccion de "Compras > Ordenes" y veras tu orden generada magicamente.

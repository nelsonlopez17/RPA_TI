# Guía del Proyecto: Gestión Integral de un ERP + Analítica + Automatización

## 1. Objetivo del Proyecto
El objetivo de este proyecto es que los estudiantes diseñen, implementen y administren un entorno empresarial simulado utilizando un sistema ERP, integrando procesos de negocio, gestión de datos, análisis y automatización. Se busca fortalecer habilidades prácticas en administración de TI, bases de datos, inteligencia de negocios y automatización de procesos.

## 2. Alcance del Proyecto
Los estudiantes deberán desarrollar un proyecto completo que incluya:
* **Implementación de un sistema ERP:** Instalación, puesta en marcha y aprovisionamiento.
* **Configuración de módulos empresariales:** Adaptación del sistema a las necesidades del negocio.
* **Administración de la base de datos:** Monitoreo y entendimiento del repositorio transaccional.
* **Consultas de información mediante SQL:** Extracción y filtrado estratégico de datos.
* **Creación de dashboards en Power BI u otro visualizador:** Capa de inteligencia de negocios interactiva.
* **Automatización de procesos con RPA:** Reducción de tareas manuales repetitivas.
* **Implementación avanzada (Opcional):** Data Warehouse, Data Lake o cubo de datos analítico.

---

## 3. Escenario de Negocio
Cada grupo deberá definir una empresa real o ficticia detallando los siguientes puntos:
* **Giro del negocio:** *Retail*, servicios, logística, manufactura, entre otros.
* **Problema que resolver:** Desafíos operativos, falta de visibilidad de datos, cuellos de botella.
* **Objetivo del uso del ERP:** Qué se espera optimizar mediante la centralización de la información.

> **Ejemplo:** Empresa de distribución que necesita controlar inventario, ventas y cuentas por cobrar para mejorar de forma crítica la toma de decisiones estratégicas.

---

## 4. Implementación del ERP

### 4.1 Instalación y Configuración
* Instalación del ERP en entorno local o en un servidor dedicado (On-Premise o Cloud).
* Configuración inicial de los parámetros del sistema.
* **Administración de TI:** Creación y parametrización de la entidad corporativa (empresa).

### 4.2 Módulos a Implementar (Mínimo 3)
El equipo debe elegir y poner en marcha al menos tres de los siguientes módulos:
* 📦 Inventario
* 💼 Ventas
* 💳 Contabilidad y Finanzas
* 🤝 CRM (Gestión de Relaciones con Clientes)
* 🛒 Compras / Abastecimiento

### 4.3 Gestión del Sistema
* Creación de usuarios y cuentas de acceso.
* Asignación de roles, perfiles y matriz de permisos de seguridad.
* Configuración y carga de **datos maestros** (clientes, proveedores, catálogo de productos, plan de cuentas).

---

## 5. Administración de Base de Datos
* Identificación y documentación del motor de base de datos subyacente (PostgreSQL, MySQL, SQL Server, etc.).
* Análisis de la estructura de tablas y el diccionario de datos.
* Identificación de relaciones entre datos, llaves primarias ($PK$) y llaves foráneas ($FK$).

### 5.1 Consultas SQL
Los estudiantes deberán diseñar y ejecutar consultas estructuradas que extraigan valor estratégico, tales como:
1.  Ventas consolidadas por período de tiempo.
2.  Top de productos más vendidos (volumen y facturación).
3.  Clientes principales (análisis de Pareto o mayor volumen de compra).
4.  Inventario disponible actual y alertas de stock mínimo.
5.  Otras consultas con indicadores críticos para el giro de negocio.

👉 **Entregable:** Script SQL (`.sql`) estructurado, optimizado y rigurosamente documentado con explicaciones detalladas para cada consulta.

---

## 6. Visualización de Datos (BI)
Utilizando **Power BI** u otra herramienta avanzada de analítica de datos, el equipo de **Administración de TI** deberá:
* Conectar el visualizador directamente a la base de datos transaccional o réplica del ERP.
* Modelar los datos y construir dashboards interactivos con filtros dinámicos.
* Generar e implementar Indicadores Clave de Rendimiento (KPIs).

### Ejemplos de Visualizaciones Requeridas:
* **Ventas Mensuales:** Evolución temporal y comparativas.
* **Margen de Ganancia:** Rentabilidad por línea de producto o categoría.
* **Rotación de Inventario:** Frecuencia de renovación de existencias en almacén.

👉 **Entregable:** Archivo original de Power BI (`.pbix`) o enlace/exportación del visualizador seleccionado.

---

## 7. Automatización de Procesos (RPA)
Se deberá diseñar, desarrollar y ejecutar la automatización de **al menos tres (3) procesos de negocio** utilizando herramientas líderes del mercado:
* *Power Automate*
* *UiPath*
* *Python* (con librerías de automatización como `pyautogui`, `selenium`, etc.)

### Ejemplos de Casos de Uso:
* Envío automático de reportes de rendimiento por correo electrónico al cierre del día.
* Registro automático de información externa (ej. facturas o tipos de cambio) dentro del ERP.
* Integración y sincronización automática de datos entre sistemas aislados.

👉 **Entregables:**
* Video demostrativo en alta definición del bot en funcionamiento (End-to-End).
* Código fuente o archivo empaquetado de automatización (`.xaml`, script `.py`, etc.).

---

## 8. Valor Agregado (Opcional)
Para aquellos equipos que busquen una **calificación superior (excelencia)**, se podrá implementar una de las siguientes soluciones de arquitectura de datos orientada a la **Administración de TI**:

* **Opción 1: Data Warehouse**
    * Diseño del modelo de datos dimensional (Tablas de Hechos y Dimensiones en esquema Estrella o Copo de Nieve).
    * Construcción e implementación de procesos ETL (Extracción, Transformación y Carga).
* **Opción 2: Data Lake**
    * Almacenamiento centralizado de datos sin procesar (estructurados y no estructurados).
    * Estrategia de transformación posterior (*Schema-on-Read*).
* **Opción 3: Cubo de Datos (OLAP)**
    * Desarrollo de un modelo analítico multidimensional optimizado para consultas de alta velocidad y reportes complejos.

---

## 9. Entregables Obligatorios

### 9.1 Documento del Proyecto
Un informe técnico formal que contenga los siguientes apartados:
1.  **Introducción:** Contexto general del proyecto.
2.  **Descripción de la Empresa:** Misión, visión, giro y problemática detectada.
3.  **Implementación del ERP:** Detalle técnico de la instalación, arquitectura y módulos activos.
4.  **Consultas SQL:** Copia del código y justificación analítica de cada script.
5.  **Visualizaciones:** Explicación del diseño del Dashboard y análisis de los KPIs obtenidos.
6.  **Automatización:** Diagrama de flujo del proceso RPA implementado y lógica del bot.
7.  **Resultados Obtenidos:** Impacto de la solución integrada en la empresa simulada.
8.  **Conclusiones:** Aprendizajes clave, retos de TI superados y recomendaciones.

### 9.2 Archivos Técnicos
* 📊 Archivo Power BI (`.pbix`).
* 💾 Scripts de Base de Datos (`.sql`).
* 🤖 Archivos de automatización (`.xaml` o scripts de código).
* 🔑 **Credenciales y accesos al sistema:**
    * Usuario y contraseña del ERP.
    * Parámetros de conexión a la Base de Datos.
    * *(Si aplica)* Accesos al Data Warehouse, Data Lake o entorno Cloud.

### 9.3 Evidencia Práctica
* Capturas de pantalla detalladas de cada fase de configuración e integración.
* Videos demostrativos del funcionamiento de los flujos.
* Matriz de pruebas realizadas con casos de éxito y manejo de excepciones.

---

## 10. Exposición del Proyecto
Cada grupo deberá realizar una defensa técnica en tiempo real donde obligatoriamente se debe:
* Mostrar el sistema ERP en producción y completamente funcional.
* Explicar la lógica técnica y de negocio detrás de las consultas SQL.
* Presentar los dashboards interactivos respondiendo a preguntas de negocio en vivo.
* Ejecutar las automatizaciones RPA en directo (*Live Demo*).
* Responder las preguntas técnicas y administrativas del comité evaluador.

---

## 11. Observaciones Finales
* ⚠️ **Sin excepciones:** No se aceptarán ni calificarán proyectos teóricos o sin evidencia práctica demostrable.
* ⚙️ El ecosistema tecnológico implementado debe ser **100% funcional** durante la evaluación.
* 👥 Se evaluará de forma diferenciada tanto el desempeño colectivo del grupo como el dominio individual de cada herramienta.
* 🔀 Se recomienda realizar una distribución clara de roles dentro del equipo de TI (ej. DBA, Desarrollador RPA, Ingeniero BI, Administrador de ERP).
* 💡 Se valorará positivamente la innovación tecnológica, la optimización del código, la seguridad informática y las buenas prácticas de TI.

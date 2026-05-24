# Guía de Despliegue: Django + Render + Supabase

## 📋 Requisitos Previos

- Cuenta en [Render.com](https://render.com)
- Cuenta en [Supabase.com](https://supabase.com)
- Repositorio en GitHub (público o privado)
- Generador de claves: https://djecrety.ir/

---

## 🚀 PASO 1: Configurar Supabase (BD)

### 1.1 Crear proyecto en Supabase
1. Ve a https://app.supabase.com
2. Haz clic en **"New project"**
3. Llena los datos:
   - **Name**: `erp-django`
   - **Password**: Guarda la contraseña (usuario: `postgres`)
   - **Region**: Elige la más cercana a tu ubicación
4. Espera a que se cree (5-10 min)

### 1.2 Obtener credenciales de Supabase
Una vez creado:
1. Ve a **Settings → Database**
2. Copia la **Connection string** (URI):
   ```
   postgresql://postgres:password@host:5432/postgres
   ```
3. Guarda esta URL, la necesitarás en Render

### 1.3 Crear usuario para Power BI (opcional pero recomendado)
1. En Supabase, ve a **SQL Editor**
2. Ejecuta este script:

```sql
-- Crear usuario solo lectura para Power BI
CREATE ROLE power_bi_user WITH LOGIN PASSWORD 'tu-contraseña-powerbi';
GRANT CONNECT ON DATABASE postgres TO power_bi_user;
GRANT USAGE ON SCHEMA public TO power_bi_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO power_bi_user;
```

---

## 🔧 PASO 2: Preparar GitHub

### 2.1 Subir proyecto a GitHub
```bash
git init
git add .
git commit -m "Initial commit - Django ERP"
git branch -M main
git remote add origin https://github.com/tu-usuario/erp-django.git
git push -u origin main
```

### 2.2 Archivos necesarios (ya están listos)
✅ `render.yaml` - Configuración de Render
✅ `requirements.txt` - Dependencias Python
✅ `.env.example` - Ejemplo de variables

### 2.3 Agregar archivo `.gitignore`
Crea un archivo `.gitignore` si no tienes (para no subir secretos):
```
.env
.env.local
*.pyc
__pycache__/
/env/
/venv/
db.sqlite3
.DS_Store
staticfiles/
```

---

## 🌐 PASO 3: Desplegar en Render

### 3.1 Conectar GitHub a Render
1. Ve a https://dashboard.render.com
2. Haz clic en **"New +"** → **"Web Service"**
3. Selecciona **"Build and deploy from a Git repository"**
4. Haz clic en **"Connect account"** (GitHub)
5. Autoriza Render en GitHub
6. Busca y selecciona tu repo `erp-django`

### 3.2 Configurar el servicio web
En la pantalla de creación:

- **Name**: `erp-django`
- **Environment**: `Python 3`
- **Region**: Igual a Supabase (o similar)
- **Branch**: `main`
- **Build Command**: (dejarlo vacío, usará render.yaml)
- **Start Command**: (dejarlo vacío, usará render.yaml)

### 3.3 Agregar variables de entorno
Haz clic en **"Advanced"** y agrega estas variables:

| Key | Value | Scope |
|-----|-------|-------|
| `DEBUG` | `False` | Public |
| `SECRET_KEY` | [Genera aquí](https://djecrety.ir/) | Secret |
| `ALLOWED_HOSTS` | `erp-django.onrender.com` | Public |
| `DB_ENGINE` | `django.db.backends.postgresql` | Public |
| `DB_HOST` | Tu host Supabase (ej: `db.xxxxx.supabase.co`) | Secret |
| `DB_NAME` | `postgres` | Secret |
| `DB_USER` | `postgres` | Secret |
| `DB_PASSWORD` | Contraseña de Supabase | Secret |
| `DB_PORT` | `5432` | Public |

### 3.4 Crear el servicio
Haz clic en **"Create Web Service"**

Render comenzará el build automáticamente. Esto toma 5-10 minutos.

### 3.5 Verificar el deploy
Una vez haya terminado:
1. Ve a la URL: `https://erp-django.onrender.com`
2. Si ves un error 500, revisa los logs en la pestaña **"Logs"**
3. Si todo está bien, verás la página de login

---

## 🔐 PASO 4: Configurar la BD en Render

### 4.1 Conectarse con PgAdmin (Desktop)
1. Descarga [PgAdmin](https://www.pgadmin.org/download/pgadmin-4-windows/)
2. Abre PgAdmin
3. Haz clic derecho en **"Servers"** → **"Register"** → **"Server"**
4. Llena:
   - **Name**: `Supabase ERP`
   - **Host**: Tu host Supabase
   - **Port**: `5432`
   - **Username**: `postgres`
   - **Password**: Tu contraseña Supabase

### 4.2 Verificar datos
Una vez conectado, verás las tablas creadas por Django:
- `inventario_producto`
- `inventario_categoria`
- `compras_ordencompra`
- `ventas_factura`
- etc.

---

## 📊 PASO 5: Conectar Power BI a Supabase

### 5.1 Instalar driver PostgreSQL
1. Descarga: [PostgreSQL ODBC Driver](https://www.postgresql.org/download/windows/)
2. Instala con las opciones por defecto

### 5.2 En Power BI Desktop
1. **Get Data** → **PostgreSQL Database**
2. Llena:
   - **Server**: Tu host Supabase
   - **Database**: `postgres`
3. **Database**: Credenciales
   - **Username**: `power_bi_user` (o `postgres` si no creaste usuario especial)
   - **Password**: Tu contraseña
4. Haz clic en **"Connect"**
5. Selecciona las tablas que necesites

---

## ✅ Checklist Final

- [ ] Proyecto en GitHub
- [ ] Supabase creado y credenciales guardadas
- [ ] Variables de entorno agregadas en Render
- [ ] Deploy completado sin errores
- [ ] Página de login accesible
- [ ] Datos migrando correctamente
- [ ] PgAdmin conectado
- [ ] Power BI conectado (si aplica)

---

## 🐛 Troubleshooting

### Error: "connection refused"
**Causa**: Variable `DB_HOST` incorrecta
**Solución**: Verifica que sea el host exacto de Supabase

### Error: "database does not exist"
**Causa**: El nombre de BD es incorrecto
**Solución**: En Supabase, la BD por defecto se llama `postgres`

### Error: "permission denied"
**Causa**: Contraseña incorrecta
**Solución**: Regenera la contraseña en Supabase

### Las migraciones no corren
**Causa**: El `buildCommand` de render.yaml no se ejecutó
**Solución**: 
1. Ve a Render Dashboard
2. Haz clic en **"Manual Deploy"** → **"Deploy latest commit"**

---

## 📞 Soporte

- [Render Docs](https://render.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [Django Deployment](https://docs.djangoproject.com/en/5.0/howto/deployment/)

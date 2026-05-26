# 🏪 Almacén Anita New Style — Sistema de Inventario

Sistema administrativo de almacén e inventario desarrollado en **Flask + MySQL**.  
Panel exclusivo para gestión interna. Sin tienda ni carrito de compras.

---

## ✅ Módulos incluidos

| Módulo | Descripción |
|---|---|
| 📦 Productos | Registro, edición, imagen, SKU, variantes (tallas/colores) |
| 📊 Stock | Control en tiempo real con alertas de stock mínimo |
| ↕️ Movimientos | Entradas, salidas, ajustes, devoluciones con historial completo |
| 🛒 Ventas físicas | Registro de ventas en tienda con buscador rápido de productos |
| 🏷️ Categorías | Clasificación de productos con ícono personalizable |
| 🚚 Proveedores | Gestión completa con RUC, contacto y notas |
| 📈 Reportes | Ventas mensuales, top productos, inventario por categoría |
| 🔐 Autenticación | Login seguro con control de sesión |

---

## 🚀 Instalación rápida

### 1. Requisitos previos
- Python 3.10+
- MySQL 8.0+ (XAMPP, WAMP o servidor propio)
- pip

### 2. Clonar / descomprimir el proyecto
```bash
cd almacen_anita
```

### 3. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar base de datos

Crear la base de datos en MySQL:
```sql
CREATE DATABASE almacen_anita_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Copiar y editar el archivo de entorno:
```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:
```
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=almacen_anita_db
```

### 6. Inicializar tablas y usuario admin
```bash
python seed.py
```
Esto crea:
- Todas las tablas
- Usuario admin: `admin@anitanewstyle.com` / `Admin2024!`
- 6 categorías base

### 7. Ejecutar el servidor
```bash
python run.py
```

Abrir en navegador: **http://localhost:5000**

---

## 🔑 Acceso inicial

| Campo | Valor |
|---|---|
| Email | admin@anitanewstyle.com |
| Contraseña | Admin2024! |

> ⚠️ Cambia la contraseña después del primer ingreso.

---

## 📁 Estructura del proyecto

```
almacen_anita/
├── app.py                  # Factory principal
├── app_extensions.py       # db, login, migrate, csrf
├── config.py               # Configuración dev/prod
├── run.py                  # Punto de entrada
├── seed.py                 # Inicialización de datos
├── requirements.txt
├── .env.example
│
├── models/
│   ├── usuario.py          # Usuarios del sistema
│   ├── producto.py         # Producto, Categoría, Proveedor
│   ├── movimiento.py       # Historial de stock
│   └── venta.py            # VentaFísica, DetalleVenta
│
├── routes/
│   ├── auth.py             # Login / logout
│   └── admin.py            # Dashboard + todos los módulos
│
├── forms/
│   ├── auth_forms.py
│   └── almacen_forms.py
│
├── templates/
│   ├── auth/login.html
│   ├── admin/
│   │   ├── base_admin.html
│   │   ├── dashboard.html
│   │   ├── productos.html
│   │   ├── producto_form.html
│   │   ├── producto_detalle.html
│   │   ├── movimientos.html
│   │   ├── movimiento_form.html
│   │   ├── ventas.html
│   │   ├── venta_form.html
│   │   ├── venta_detalle.html
│   │   ├── categorias.html
│   │   ├── categoria_form.html
│   │   ├── proveedores.html
│   │   ├── proveedor_form.html
│   │   └── reportes.html
│   └── errores/404.html, 500.html
│
└── static/
    ├── css/admin.css
    └── img/productos/      # Imágenes de productos
```

---

## 🔄 Flujo de trabajo recomendado

1. **Configurar categorías** → Almacén > Categorías
2. **Registrar proveedores** → Almacén > Proveedores
3. **Ingresar productos** → Almacén > Productos > Nuevo
4. **Registrar entradas de mercadería** → Movimientos > Nuevo (tipo: Entrada)
5. **Registrar ventas** → Ventas > Nueva venta
6. **Revisar reportes** → Reportes

---

## 🛠️ Tecnologías

- **Backend:** Python 3 + Flask 3.0
- **ORM:** SQLAlchemy + Flask-Migrate
- **Base de datos:** MySQL 8
- **Frontend:** Bootstrap 5 + Bootstrap Icons
- **Gráficos:** Chart.js 4
- **Seguridad:** Flask-Login + Flask-WTF (CSRF)

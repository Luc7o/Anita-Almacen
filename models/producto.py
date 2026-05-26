from datetime import datetime
import json
from app_extensions import db


class Categoria(db.Model):
    __tablename__ = 'categorias'

    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(80), nullable=False, unique=True)
    slug        = db.Column(db.String(80), nullable=False, unique=True)
    descripcion = db.Column(db.String(300))
    icono       = db.Column(db.String(50), default='box-seam')
    activo      = db.Column(db.Boolean, default=True)
    productos   = db.relationship('Producto', backref='categoria', lazy='dynamic')

    def __repr__(self):
        return f'<Categoria {self.nombre}>'


class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(150), nullable=False)
    ruc         = db.Column(db.String(11), unique=True)
    contacto    = db.Column(db.String(100))
    telefono    = db.Column(db.String(20))
    email       = db.Column(db.String(150))
    direccion   = db.Column(db.String(250))
    activo      = db.Column(db.Boolean, default=True)
    notas       = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    productos   = db.relationship('Producto', backref='proveedor', lazy='dynamic')
    movimientos = db.relationship('MovimientoStock', backref='proveedor', lazy='dynamic')

    def __repr__(self):
        return f'<Proveedor {self.nombre}>'


class Producto(db.Model):
    __tablename__ = 'productos'

    id              = db.Column(db.Integer, primary_key=True)
    nombre          = db.Column(db.String(150), nullable=False)
    descripcion     = db.Column(db.Text)
    sku             = db.Column(db.String(60), unique=True)
    codigo_barras   = db.Column(db.String(100))
    categoria_id    = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    proveedor_id    = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=True)

    # Precios
    precio_compra   = db.Column(db.Numeric(10, 2), default=0)
    precio_venta    = db.Column(db.Numeric(10, 2), nullable=False)

    # Stock
    stock           = db.Column(db.Integer, default=0)
    stock_minimo    = db.Column(db.Integer, default=5)   # alerta de stock bajo

    # Variantes
    tallas          = db.Column(db.Text)   # JSON: ["36","37","38"]
    colores         = db.Column(db.Text)   # JSON: ["Negro","Blanco"]
    unidad          = db.Column(db.String(30), default='unidad')  # unidad, par, caja...

    # Imagen
    imagen_principal = db.Column(db.String(300), default='no-imagen.png')

    # Estado
    activo          = db.Column(db.Boolean, default=True)
    fecha_creacion  = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualiz  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    movimientos     = db.relationship('MovimientoStock', backref='producto', lazy='dynamic')
    detalles_venta  = db.relationship('DetalleVenta', backref='producto', lazy='dynamic')

    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo

    @property
    def sin_stock(self):
        return self.stock <= 0

    @property
    def tallas_lista(self):
        if self.tallas:
            try:
                return json.loads(self.tallas)
            except Exception:
                return self.tallas.split(',')
        return []

    @property
    def colores_lista(self):
        if self.colores:
            try:
                return json.loads(self.colores)
            except Exception:
                return self.colores.split(',')
        return []

    @property
    def margen(self):
        if self.precio_compra and float(self.precio_compra) > 0:
            return round((float(self.precio_venta) - float(self.precio_compra)) / float(self.precio_compra) * 100, 1)
        return None

    @property
    def valor_inventario(self):
        return float(self.precio_venta) * self.stock

    def __repr__(self):
        return f'<Producto {self.nombre}>'

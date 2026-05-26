from datetime import datetime
from app_extensions import db


class MovimientoStock(db.Model):
    __tablename__ = 'movimientos_stock'

    TIPOS = {
        'entrada':  ('Entrada',  'success', 'box-arrow-in-down'),
        'salida':   ('Salida',   'danger',  'box-arrow-up'),
        'ajuste':   ('Ajuste',   'warning', 'arrow-left-right'),
        'venta':    ('Venta',    'info',    'cart-check'),
        'devolucion':('Devolución','secondary','arrow-return-left'),
    }

    id           = db.Column(db.Integer, primary_key=True)
    producto_id  = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    tipo         = db.Column(db.String(20), nullable=False)   # entrada|salida|ajuste|venta|devolucion
    cantidad     = db.Column(db.Integer, nullable=False)
    stock_antes  = db.Column(db.Integer, nullable=False)
    stock_despues= db.Column(db.Integer, nullable=False)
    motivo       = db.Column(db.String(250))
    referencia   = db.Column(db.String(100))  # Nro factura, venta, etc.
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=True)
    usuario_id   = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    fecha        = db.Column(db.DateTime, default=datetime.utcnow)

    usuario      = db.relationship('Usuario', backref='movimientos')

    @property
    def tipo_label(self):
        return self.TIPOS.get(self.tipo, ('Desconocido','secondary','question'))[0]

    @property
    def tipo_color(self):
        return self.TIPOS.get(self.tipo, ('Desconocido','secondary','question'))[1]

    @property
    def tipo_icono(self):
        return self.TIPOS.get(self.tipo, ('Desconocido','secondary','question'))[2]

    def __repr__(self):
        return f'<Movimiento {self.tipo} prod={self.producto_id} cant={self.cantidad}>'

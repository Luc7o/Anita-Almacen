from datetime import datetime
import uuid
from app_extensions import db


class VentaFisica(db.Model):
    __tablename__ = 'ventas_fisicas'

    METODOS_PAGO = {
        'efectivo':  'Efectivo',
        'yape':      'Yape / Plin',
        'tarjeta':   'Tarjeta',
        'transferencia': 'Transferencia',
    }

    id              = db.Column(db.Integer, primary_key=True)
    numero_venta    = db.Column(db.String(30), unique=True, nullable=False)
    cliente_nombre  = db.Column(db.String(150))
    cliente_doc     = db.Column(db.String(15))
    metodo_pago     = db.Column(db.String(20), nullable=False, default='efectivo')
    subtotal        = db.Column(db.Numeric(10, 2), nullable=False)
    descuento       = db.Column(db.Numeric(10, 2), default=0)
    total           = db.Column(db.Numeric(10, 2), nullable=False)
    notas           = db.Column(db.Text)
    usuario_id      = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    fecha           = db.Column(db.DateTime, default=datetime.utcnow)
    anulada         = db.Column(db.Boolean, default=False)

    detalles        = db.relationship('DetalleVenta', backref='venta', lazy='dynamic',
                                      cascade='all, delete-orphan')
    usuario         = db.relationship('Usuario', backref='ventas')

    @staticmethod
    def generar_numero():
        return f"V-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:5].upper()}"

    @property
    def metodo_pago_label(self):
        return self.METODOS_PAGO.get(self.metodo_pago, self.metodo_pago)

    def __repr__(self):
        return f'<VentaFisica {self.numero_venta}>'


class DetalleVenta(db.Model):
    __tablename__ = 'detalles_venta'

    id          = db.Column(db.Integer, primary_key=True)
    venta_id    = db.Column(db.Integer, db.ForeignKey('ventas_fisicas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad    = db.Column(db.Integer, nullable=False, default=1)
    precio_unit = db.Column(db.Numeric(10, 2), nullable=False)
    talla       = db.Column(db.String(20))
    color       = db.Column(db.String(50))
    subtotal    = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<DetalleVenta venta={self.venta_id} prod={self.producto_id}>'

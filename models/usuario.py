from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app_extensions import db


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id              = db.Column(db.Integer, primary_key=True)
    nombre          = db.Column(db.String(100), nullable=False)
    apellido        = db.Column(db.String(100), nullable=False)
    email           = db.Column(db.String(150), unique=True, nullable=False)
    password_hash   = db.Column(db.String(256), nullable=False)
    es_admin        = db.Column(db.Boolean, default=False)  # BUG CORREGIDO: default False, no True
    activo          = db.Column(db.Boolean, default=True)
    fecha_registro  = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acceso   = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def __repr__(self):
        return f'<Usuario {self.email}>'

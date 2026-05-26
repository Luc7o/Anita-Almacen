"""
Ejecutar una sola vez para crear las tablas y el usuario administrador.
  python seed.py
"""
from app import create_app
from app_extensions import db
from models.usuario import Usuario
from models.producto import Categoria

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tablas creadas.")

    # Admin por defecto
    if not Usuario.query.filter_by(email='admin@anitanewstyle.com').first():
        admin = Usuario(
            nombre='Administrador', apellido='Sistema',
            email='admin@anitanewstyle.com', es_admin=True, activo=True
        )
        admin.set_password('Admin2024!')
        db.session.add(admin)
        print("✅ Usuario admin creado: admin@anitanewstyle.com / Admin2024!")

    # Categorías base
    cats_default = [
        ('Calzados',   'calzados',   'boot'),
        ('Vestidos',   'vestidos',   'bag'),
        ('Carteras',   'carteras',   'handbag'),
        ('Mochilas',   'mochilas',   'backpack'),
        ('Accesorios', 'accesorios', 'gem'),
        ('Ropa',       'ropa',       'tags'),
    ]
    for nombre, slug, icono in cats_default:
        if not Categoria.query.filter_by(slug=slug).first():
            db.session.add(Categoria(nombre=nombre, slug=slug, icono=icono))

    db.session.commit()
    print("✅ Categorías base creadas.")
    print("\n🚀 Sistema listo. Ejecuta: python run.py")

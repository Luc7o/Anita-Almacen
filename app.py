import os
from flask import Flask, render_template, redirect, url_for
from config import config
from app_extensions import db, login, migrate, csrf


def create_app(env=None):
    app = Flask(__name__)
    env = env or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config.get(env, config['default']))

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from models.usuario import Usuario

    @login.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Blueprints
    from routes.auth  import bp as auth_bp
    from routes.admin import bp as admin_bp

    app.register_blueprint(auth_bp,  url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Redirigir raíz al dashboard
    @app.route('/')
    def index():
        return redirect(url_for('admin.dashboard'))

    # Filtros Jinja
    @app.template_filter('moneda')
    def filtro_moneda(valor):
        return f"S/ {float(valor or 0):.2f}"

    @app.template_filter('fecha_corta')
    def filtro_fecha_corta(dt):
        return dt.strftime('%d/%m/%Y') if dt else '—'

    @app.template_filter('fecha_hora')
    def filtro_fecha_hora(dt):
        return dt.strftime('%d/%m/%Y %H:%M') if dt else '—'

    # Errores
    @app.errorhandler(404)
    def pagina_no_encontrada(e):
        return render_template('errores/404.html'), 404

    @app.errorhandler(500)
    def error_servidor(e):
        return render_template('errores/500.html'), 500

    return app

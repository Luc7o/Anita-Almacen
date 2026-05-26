from datetime import datetime
from urllib.parse import urlparse
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app_extensions import db
from models.usuario import Usuario
from forms.auth_forms import FormLogin

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data.lower().strip()).first()
        if usuario and usuario.check_password(form.password.data):
            if not usuario.activo:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'danger')
                return redirect(url_for('auth.login'))
            login_user(usuario, remember=form.recordar.data)
            usuario.ultimo_acceso = datetime.utcnow()
            db.session.commit()
            next_page = request.args.get('next')
            # BUG CORREGIDO: Prevenir Open Redirect — solo permitir rutas internas
            if next_page:
                parsed = urlparse(next_page)
                if parsed.netloc or parsed.scheme:
                    next_page = None
            return redirect(next_page or url_for('admin.dashboard'))
        flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))

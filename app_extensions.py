from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

db      = SQLAlchemy()
login   = LoginManager()
migrate = Migrate()
csrf    = CSRFProtect()

login.login_view     = 'auth.login'
login.login_message  = 'Inicia sesión para acceder al sistema.'
login.login_message_category = 'warning'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class FormLogin(FlaskForm):
    email    = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=4)])
    recordar = BooleanField('Mantener sesión')
    submit   = SubmitField('Ingresar')

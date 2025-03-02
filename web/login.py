from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from flask_jwt_extended import decode_token, exceptions



class LoginForm(FlaskForm):
    """Formulario de inicio de sesión que espera los campos de nombre de usuario y contraseña de un administrador"""
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')



def is_authenticated():
    """ Verifica si el usuario está autenticado """
    try:
        token = request.cookies.get("access_token")

        if token:
            # Intenta decodificar el token (si es válido)
            decode_token(token)
            return True

    except exceptions.JWTExtendedException:
        # Si hay cualquier error con el token, consideramos que no está autenticado
        pass

    return False
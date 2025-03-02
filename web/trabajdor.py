from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, Optional



class TrabajadorForm(FlaskForm):
    """Formulario que recibe los datos de un trabajador. Puede ser configurado para requerir o no la contraseña."""

    nif = StringField("NIF", validators=[InputRequired(), Length(min=9, max=9)])
    nombre = StringField("Nombre", validators=[InputRequired(), Length(min=1, max=255)])
    telefono = StringField("Teléfono", validators=[InputRequired(), Length(min=9, max=9)])
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=30)])

    # Contraseña opcional o requerida dependiendo de la variable password_required
    password = PasswordField("Contraseña")

    submit = SubmitField("Guardar cambios")

    def __init__(self, *args, **kwargs):
        # Obtener el parámetro de si la contraseña es obligatoria o no
        password_required = kwargs.pop("password_required", False)
        super().__init__(*args, **kwargs)

        # Si la contraseña es obligatoria, configuramos el validador de InputRequired()
        if password_required:
            self.password.validators = [InputRequired()]

        else:
            self.password.validators = [Optional()]

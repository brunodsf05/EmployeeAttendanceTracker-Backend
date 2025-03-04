from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, DateField, TimeField
from wtforms.validators import Optional



class MyTimeForm(FlaskForm):
    """
    Formulario para modificar la fecha y horas del servidor.
    Puede alternar entre usar la fecha y hora actuales o especificar una fecha y hora estáticas,
    esto último perfecto para depurar.
    """
    use_now = BooleanField("Usar tiempo actual")
    date = DateField("Fecha", validators=[Optional()])
    time = TimeField("Hora", validators=[Optional()])
    submit = SubmitField("Enviar")
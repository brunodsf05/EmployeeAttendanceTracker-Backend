from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import InputRequired, ValidationError



def validar_latitud(form, field):
    if field.data < -90 or field.data > 90:
        raise ValidationError('La latitud debe estar entre -90 y 90.')

def validar_longitud(form, field):
    if field.data < -180 or field.data > 180:
        raise ValidationError('La longitud debe estar entre -180 y 180.')



class EmpresaForm(FlaskForm):
    """Formulario para modificar los datos de una empresa. Por defecto viene con los campos ya rellenos, listos para ser cambiados."""

    nombre = StringField("Nombre de la empresa", validators=[InputRequired()])
    latitud = FloatField("Latitud", validators=[InputRequired(), validar_latitud])
    longitud = FloatField("Longitud", validators=[InputRequired(), validar_longitud])
    radio = IntegerField("Radio (en metros)", validators=[InputRequired()])
    submit = SubmitField("Guardar cambios")
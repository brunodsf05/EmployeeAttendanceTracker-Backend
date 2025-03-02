from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired

from models import Empresa



class EmpresaForm(FlaskForm):
    """Formulario para modificar los datos de una empresa. Por defecto viene con los campos ya rellenos, listos para ser cambiados."""

    nombre = StringField("Nombre de la empresa", validators=[DataRequired()])
    latitud = FloatField("Latitud", validators=[DataRequired()])
    longitud = FloatField("Longitud", validators=[DataRequired()])
    radio = IntegerField("Radio (en metros)", validators=[DataRequired()])
    submit = SubmitField("Guardar cambios")

    def __init__(self, *args, **kwargs):
        empresa = Empresa.get_first()

        if empresa:
            self.nombre.data = empresa.nombre
            self.latitud.data = empresa.latitud
            self.longitud.data = empresa.longitud
            self.radio.data = empresa.radio

        super().__init__(*args, **kwargs)

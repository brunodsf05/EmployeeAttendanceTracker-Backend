from extensions import db
from datetime import datetime
from .franja_horaria import FranjaHoraria



class Horario(db.Model):
    __tablename__ = "horarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_nombre(cls, nombre):
        return cls.query.filter_by(nombre=nombre).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def data(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

    def get_franjahoraria_by_date(self, fecha):
        dia_id = fecha.weekday() + 1  # Asumiendo que el id del día comienza en 1 para Lunes
        return FranjaHoraria.query.filter_by(dia_id=dia_id, horario_id=self.id).first()
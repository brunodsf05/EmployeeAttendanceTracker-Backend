from extensions import db
from enum import Enum



class Registro(db.Model):
    __tablename__ = "registros"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora_entrada = db.Column(db.Time, nullable=False)
    hora_salida = db.Column(db.Time, nullable=False)

    trabajador_id = db.Column(db.Integer, db.ForeignKey("trabajadores.id"))
    trabajador = db.relationship("Trabajador", backref=db.backref("registros", lazy=True))

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def data(self):
        trabajador_data = {} if self.trabajador == None else self.trabajador.data

        return {
            "id": self.id,
            "fecha": self.fecha.isoformat(),
            "hora_entrada": self.hora_entrada.isoformat(),
            "hora_salida": self.hora_salida.isoformat(),
            "trabajador": trabajador_data
        }



class AccionesRegistro(Enum):
    """
    Esto describe las acciones que debe realizar un trabajador sobre los fichajes.
    Ejemplo: Si un trabajador entra a las 3:00 pero son las 2:00, debe esperar (WAIT).
    """
    WAIT = "WAIT"
    START = "START"
    WORK = "WORK"
    EXIT = "EXIT"
    RECOVER = "RECOVER"
    NOTIFY_AUSENCE = "NOTIFY_AUSENCE"
    TOBEIN_WORK = "TOBEIN_WORK"

    @staticmethod
    def get_from_trabajador(trabajador, tiempo):
        return None

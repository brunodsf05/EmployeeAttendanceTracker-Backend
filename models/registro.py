from extensions import db



class Registro(db.Model):
    __tablename__ = "registros"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora_entrada = db.Column(db.Time, nullable=True)
    hora_salida = db.Column(db.Time, nullable=True)

    trabajador_id = db.Column(db.Integer, db.ForeignKey("trabajadores.id", ondelete="RESTRICT"))
    trabajador = db.relationship("Trabajador", backref=db.backref("registros", lazy=True))

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_all_weird_from_trabajador(cls, trabajador):
        """ Lista todos los registros de un trabajador que no sean correctos. Ejemplo: Les falta la salida, etc... """
        return cls.query.all()

    @classmethod
    def get_all_good_from_trabajador(cls, trabajador):
        """ Lista todos los registros de un trabajador que tenga entrada y salida correctas """
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
from extensions import db



class Incidencia(db.Model):
    __tablename__ = "incidencias"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.String(255))

    trabajador_id = db.Column(db.Integer, db.ForeignKey("trabajadores.id"))
    trabajador = db.relationship("Trabajador", backref=db.backref("incidencias", lazy=True))


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
            "descripcion": self.descripcion,
            "trabajador": trabajador_data
        }
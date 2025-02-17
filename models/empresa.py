from extensions import db



class Empresa(db.Model):
    __tablename__ = "empresas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    radio = db.Column(db.Integer)

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
            "latitud": self.latitud,
            "longitud": self.longitud,
            "radio": self.radio
        }
from extensions import db;

class Receta(db.Model):
    __tablename__ = "recetas"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100,), nullable=False)
    descripcion = db.Column(db.String(200))
    raciones = db.Column(db.Integer)
    tiempo = db.Column(db.Integer)
    pasos = db.Column(db.String(1000))
    es_publicada = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_by_nombre(cls, nombre):
        return cls.query.filter_by(nombre=nombre).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    @property
    def data(self):
        """
        Retorna la receta como si fuese un diccionario, es decir, pares nombre:valor,
        Esto es especialmente útil para enviar los datos en una respuesta de la api rest.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "raciones": self.raciones,
            "tiempo": self.tiempo,
            "pasos": self.pasos,
            "es_publicada": self.es_publicada,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
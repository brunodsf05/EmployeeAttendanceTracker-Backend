from extensions import db



class FranjaHoraria(db.Model):
    __tablename__ = "franjas_horarias"

    id = db.Column(db.Integer, primary_key=True)
    hora_entrada = db.Column(db.Time, nullable=False)
    hora_salida = db.Column(db.Time, nullable=False)

    horario_id = db.Column(db.Integer, db.ForeignKey("horarios.id", ondelete="CASCADE"))
    dia_id = db.Column(db.Integer, db.ForeignKey("dias.id", ondelete="RESTRICT"))

    horario = db.relationship("Horario", backref=db.backref("franjas_horarias", lazy=True))
    dia = db.relationship("Dia", backref=db.backref("franjas_horarias", lazy=True))

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
        horario_data = {} if self.horario == None else self.horario.data
        dia_data = {} if self.dia == None else self.dia.data

        return {
            "id": self.id,
            "hora_entrada": self.hora_entrada.isoformat(),
            "hora_salida": self.hora_salida.isoformat(),
            "horario": horario_data,
            "dia": dia_data
        }
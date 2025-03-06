from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db



class Trabajador(db.Model):
    __tablename__ = "trabajadores"

    id = db.Column(db.Integer, primary_key=True)
    nif = db.Column(db.String(20))
    nombre = db.Column(db.String(255))
    telefono = db.Column(db.String(9))
    debaja = db.Column(db.Boolean(), default=True, nullable=False)

    username = db.Column(db.String(30), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)

    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="RESTRICT"))
    horario_id = db.Column(db.Integer, db.ForeignKey("horarios.id", ondelete="RESTRICT"))
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"))

    rol = db.relationship("Rol", backref=db.backref("trabajadores", lazy=True))
    horario = db.relationship("Horario", backref=db.backref("trabajadores", lazy=True))
    empresa = db.relationship("Empresa", backref=db.backref("trabajadores", lazy=True))

    @property
    def password(self):
        """La contraseña hasheada"""
        return self._password

    @password.setter
    def password(self, password_plaintext):
        """Hashea la contraseña antes de guardarla"""
        self._password = generate_password_hash(password_plaintext)

    def check_password(self, password_plaintext):
        """Verifica si la contraseña ingresada es correcta"""
        # HACK: Si está de baja, no puede entrar
        if self.debaja:
            return False

        return check_password_hash(self._password, password_plaintext)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_username(cls, username):
        """ Busca a un empleado por su nombre de usuario. No es case sensitive. """
        return cls.query.filter(Trabajador.username.ilike(username)).first()

    @classmethod
    def get_by_nif(cls, nif):
        """ Busca a un empleado por su NIF. No es case sensitive. """
        return cls.query.filter(Trabajador.nif.ilike(nif)).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_all_activos(cls):
        return cls.query.filter_by(debaja=False).all()

    @classmethod
    def get_all_debaja(cls):
        return cls.query.filter_by(debaja=True).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def data(self):
        rol_data = {} if self.rol == None else self.rol.data
        horario_data = {} if self.horario == None else self.horario.data
        empresa_data = {} if self.empresa == None else self.empresa.data

        return {
            "id": self.id,
            "nif": self.nif,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "username": self.username,
            "password": self.password,
            "rol": rol_data,
            "horario": horario_data,
            "empresa": empresa_data
        }
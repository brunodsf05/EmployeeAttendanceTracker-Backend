from extensions import db

import math


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

    @classmethod
    def get_first(cls):
        empresas = cls.get_all()

        return None if len(empresas) == 0 else empresas[0]

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_inside(self, latitud, longitud):
        """
        Verifica si un punto (latitud, longitud) está dentro del radio de la empresa.
        Devuelve True si está dentro, False en caso contrario.
        """
        # Radio de la Tierra en kilómetros
        R = 6371.0
        
        # Convertir grados a radianes
        lat1_rad = math.radians(latitud)
        lon1_rad = math.radians(longitud)
        lat2_rad = math.radians(self.latitud)
        lon2_rad = math.radians(self.longitud)
        
        # Diferencias de coordenadas
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        
        # Fórmula de Haversine
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distancia = R * c
        
        # Verificar si la distancia es menor o igual al radio
        return distancia <= self.radio

    @property
    def data(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "radio": self.radio
        }
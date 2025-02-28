from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from enum import Enum
from datetime import datetime

from models import Registro, Trabajador



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



class FichajeResource(Resource):
    """Maneja el fichaje de entrada y salida de los trabajadores"""

    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        trabajador = Trabajador.get_by_username(username)

        if not trabajador:
            return {"message": "Trabajador no encontrado"}, HTTPStatus.NOT_FOUND

        # Obtener registro de hoy
        today = datetime.now().date()
        registro = Registro.query.filter_by(trabajador_id=trabajador.id, fecha=today).first()

        if registro is None:
            # No hay registro, se debe fichar entrada
            hora_actual = datetime.now().time()
            if hora_actual < trabajador.horario.franja_horaria.hora_entrada:
                return {"message": "Debes esperar a fichar entrada"}, HTTPStatus.BAD_REQUEST
            elif hora_actual >= trabajador.horario.franja_horaria.hora_salida:
                return {"message": "No has ido al trabajo"}, HTTPStatus.BAD_REQUEST
            else:
                # Fichar entrada
                nuevo_registro = Registro(fecha=today, hora_entrada=hora_actual)
                nuevo_registro.trabajador = trabajador
                nuevo_registro.save()
                return {"message": "Fichaje de entrada registrado"}, HTTPStatus.CREATED
        else:
            # Ya hay un registro, verificar si puede fichar salida
            if registro.hora_salida is not None:
                return {"message": "Ya has fichado salida"}, HTTPStatus.BAD_REQUEST

            hora_actual = datetime.now().time()
            if hora_actual < trabajador.horario.franja_horaria.hora_salida:
                return {"message": "Aún no puedes fichar salida"}, HTTPStatus.BAD_REQUEST
            else:
                # Fichar salida
                registro.hora_salida = hora_actual
                registro.save()
                return {"message": "Fichaje de salida registrado"}, HTTPStatus.OK
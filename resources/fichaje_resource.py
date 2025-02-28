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
    WAIT = "WAIT" # Debes esperar a que sea la hora de entrada
    START = "START" # Debes iniciar tu jornada laboral
    WORK = "WORK" # Todavía no se ha terminado la jornada laboral
    EXIT = "EXIT" # Ya puedes salir del trabajo
    RECOVER = "RECOVER" # Ya fichastes la salida
    NOTIFY_AUSENCE = "NOTIFY_AUSENCE" # No fichastes la entrada
    TOBEIN_WORK = "TOBEIN_WORK"  # No te encuentras en el lugar de trabajo
    FREEDAY = "FREEDAY" # Hoy no trabajas

    def __str__(self):
        return self.value

    @staticmethod
    def get_from_trabajador(trabajador: Trabajador, tiempo: datetime):
        # Conseguir la franja horaria del trabajador
        franja_horaria = trabajador.horario.get_franjahoraria_by_date(tiempo)

        if franja_horaria is None:
            return AccionesRegistro.FREEDAY

        # Conseguir horas
        hora_entrada = franja_horaria.hora_entrada
        hora_salida = franja_horaria.hora_entrada

        return { "id": franja_horaria.id, "hora_entrada": hora_entrada.isoformat(), "hora_salida": hora_salida.isoformat()}



class FichajeResource(Resource):
    """Maneja el fichaje de entrada y salida de los trabajadores"""

    @jwt_required()
    def get(self):
        # Obtener trabajador de la petición
        username = get_jwt_identity()
        trabajador = Trabajador.get_by_username(username)

        if trabajador is None:
            return {"error": "usernotfound"}, HTTPStatus.NOT_FOUND

        if trabajador.horario is None:
            return {"error": "horarionotfound"}, HTTPStatus.NOT_FOUND

        # Conseguir accion
        return {
            "trabajador": trabajador.nombre,
            "accion": AccionesRegistro.get_from_trabajador(trabajador, datetime.now())
        }, HTTPStatus.OK

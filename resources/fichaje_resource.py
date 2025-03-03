from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from enum import Enum
from datetime import datetime

from models import Registro, Trabajador
from mytime import MyTime



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
        """Consigue la acción que debe realizar el trabajador en el tiempo dado.
        No tiene en cuenta la geolocalización del trabajador, por lo esa parte se debe manejar aparte.
        """
        # Conseguir la franja horaria del trabajador
        franja_horaria = trabajador.horario.get_franjahoraria_by_date(tiempo)

        if franja_horaria is None:
            return AccionesRegistro.FREEDAY

        # Conseguir horas
        hora_actual = tiempo.time()
        hora_entrada = franja_horaria.hora_entrada
        hora_salida = franja_horaria.hora_salida

        # Condiciones con nombre limpio
        no_puede_entrar = hora_actual < hora_entrada
        es_hora_laboral = hora_actual < hora_salida

        # Conseguir accion
        if no_puede_entrar:
            return AccionesRegistro.WAIT

        registro = Registro.query.filter_by(trabajador_id=trabajador.id, fecha=tiempo.date()).first()

        # Todavía no se registró la entrada
        if registro is None:
            if es_hora_laboral:
                return AccionesRegistro.START
            else:
                return AccionesRegistro.NOTIFY_AUSENCE

        if registro.hora_entrada is None:
            return AccionesRegistro.START

        # Todavía no se registró la salida
        if registro.hora_salida is None:
            if es_hora_laboral:
                return AccionesRegistro.WAIT
            else:
                return AccionesRegistro.EXIT

        # Ya realizó su jornada laboral
        return AccionesRegistro.RECOVER



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
        tiempo_actual = MyTime.get()
        accion = AccionesRegistro.get_from_trabajador(trabajador, tiempo_actual)

        # Conseguir horas
        hora_entrada,hora_salida = None, None

        franja_horaria = trabajador.horario.get_franjahoraria_by_date(tiempo_actual)

        if franja_horaria is not None:
            hora_entrada = franja_horaria.hora_entrada
            hora_salida = franja_horaria.hora_salida

        return {
            "action": str(accion),
            "hora_entrada": hora_entrada.isoformat(),
            "hora_salida": hora_salida.isoformat(),
            "debug": {
                "today": tiempo_actual.isoformat(),
                "horario": {
                    "id": trabajador.horario.id,
                    "nombre": trabajador.horario.nombre,
                }
            }
        }, HTTPStatus.OK

    @jwt_required()
    def post(self):
        # Obtener trabajador de la petición
        username = get_jwt_identity()
        trabajador = Trabajador.get_by_username(username)

        if trabajador is None:
            return {"error": "usernotfound"}, HTTPStatus.NOT_FOUND

        if trabajador.horario is None:
            return {"error": "horarionotfound"}, HTTPStatus.NOT_FOUND

        if trabajador.empresa is None:
            return {"error": "empresanotfound"}, HTTPStatus.NOT_FOUND

        # Leer ubicación
        data = request.get_json()

        try:
            user_latitude = float(data["latitude"])
            user_longitude = float(data["longitude"])

        except (ValueError, TypeError, KeyError):
            return {"error": "invalidlocation"}, HTTPStatus.BAD_REQUEST

        is_inside_empresa = trabajador.empresa.is_inside(user_latitude, user_longitude)

        # Conseguir accion
        tiempo_actual = MyTime.get()
        accion = AccionesRegistro.get_from_trabajador(trabajador, tiempo_actual)

        # Manejar acción y ubicación
        if not is_inside_empresa:
            return {"error": "isnotinside"}, HTTPStatus.METHOD_NOT_ALLOWED

        match accion:
            case AccionesRegistro.START:
                # Registrar entrada
                registro = Registro(trabajador_id=trabajador.id, fecha=tiempo_actual.date(), hora_entrada=tiempo_actual.time())
                registro.save()
                return {"action": str(AccionesRegistro.WORK)}, HTTPStatus.OK
            
            case AccionesRegistro.EXIT:
                # Registrar salida
                registro = Registro.query.filter_by(trabajador_id=trabajador.id, fecha=tiempo_actual.date()).first()
                registro.hora_salida = tiempo_actual.time()
                registro.save()
                return {"action": str(AccionesRegistro.RECOVER)}, HTTPStatus.OK

        # No se pudo realizar el fichaje
        return {"error": "couldntclock"}, HTTPStatus.METHOD_NOT_ALLOWED
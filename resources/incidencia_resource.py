from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from enum import Enum
from datetime import datetime, time

from models import Incidencia, Trabajador
from mytime import MyTime



class IncidenciaResource(Resource):
    """Almacena las incidencias creadas por los trabajadores"""

    @jwt_required()
    def post(self):
        # Obtener trabajador de la petición
        username = get_jwt_identity()
        trabajador = Trabajador.get_by_username(username)

        if trabajador is None:
            return {"error": "usernotfound"}, HTTPStatus.NOT_FOUND

        # Leer ubicación
        data = request.get_json()

        try:
            incidencia_datetime = datetime.strptime(data["datetime"], "%Y-%m-%dT%H:%M:%SZ")
            incidencia_description = data["description"]

            Incidencia(
                fecha=incidencia_datetime,
                descripcion=incidencia_description,
                trabajador=trabajador
            ).save()

        except Exception:
            return {"error": "badrequest"}, HTTPStatus.BAD_REQUEST

        return data, HTTPStatus.OK
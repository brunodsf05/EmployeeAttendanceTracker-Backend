from flask import request
from flask_restful import Resource
from http import HTTPStatus



from models import Trabajador



class LoginResource(Resource):
    """Maneja el inicio de sesión"""

    def post(self):
        """
        Recibe las credenciales de usuario para devolver un token se sesión.
        En caso de que no se pueda devolver un token, devolvemos un código de error.

        Entrada:
            { "username": ..., "password": ... }

        Salida: ¿Se devuelve un token?
            Sí { "success": True, "token": ... }
            No { "success": False, "error": ... }
        """
        # Leer petición
        data = request.get_json()

        username = data["username"]
        password = data["password"]

        trabajador = Trabajador.get_by_username(username)

        # Validaciones
        if trabajador == None:
            return {"success": False, "error": "usernotfound"}, HTTPStatus.OK

        if password != trabajador.password:
            return {"success": False, "error": "incorrectpassword"}, HTTPStatus.OK

        # Devolver token
        token = "temp"

        return {"success": True, "token": token}, HTTPStatus.OK
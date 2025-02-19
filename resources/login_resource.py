from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from http import HTTPStatus


from models import Trabajador



class LoginResource(Resource):
    """Maneja el inicio de sesión"""

    def post(self):
        """
        Recibe las credenciales de usuario para devolver un token se sesión.
        En caso de que no se pueda devolver un token, devolvemos un código de error.

        Entrada:
            { "username": "...", "password": "..." }

        Salida: ¿Se devuelve un token?
            Sí { "success": True, "access_token": "...", "refresh_token": "..." }
            No { "success": False, "error": "..." }
        """
        # Leer petición
        data = request.get_json()

        username = data["username"]
        password = data["password"]

        trabajador = Trabajador.get_by_username(username)

        # Validaciones
        if trabajador == None:
            return {"success": False, "error": "usernotfound"}, HTTPStatus.UNAUTHORIZED

        if not trabajador.check_password(password):
            return {"success": False, "error": "incorrectpassword"}, HTTPStatus.UNAUTHORIZED

        # Devolver token
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return {"success": True, "access_token": access_token, "refresh_token": refresh_token}, HTTPStatus.OK
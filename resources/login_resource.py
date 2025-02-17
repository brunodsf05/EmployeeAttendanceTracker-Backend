from flask import request
from flask_restful import Resource
from http import HTTPStatus



from models import Receta



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
        datos = request.get_json()

        username = datos["username"]
        password = datos["password"]

        """
        if Receta.get_by_nombre(nombre_receta):
            return {"message": "Ya existe una receta con ese nombre"}, HTTPStatus.BAD_REQUEST

        receta = Receta(
            nombre = nombre_receta,
            descripcion = datos["descripcion"],
            raciones = datos["raciones"],
            tiempo = datos["tiempo"],
            pasos = datos["pasos"],
        )

        receta.guardar()
        """

        return {"success": False, "error": "usernotfound"}, HTTPStatus.OK
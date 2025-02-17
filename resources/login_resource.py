from flask import request
from flask_restful import Resource
from http import HTTPStatus



from models import Receta



class LoginResource(Resource):
    """Maneja el inicio de sesión"""

    def post(self):
        """
        Espera un "user" y "password" podrá devolver un token o un mensaje de error.
        """
        datos = request.get_json()

        user = datos["user"]
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

        return {"success": False, "message": "usernotfound"}, HTTPStatus.OK
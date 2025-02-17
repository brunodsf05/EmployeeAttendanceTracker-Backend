from flask import request
from flask_restful import Resource
from http import HTTPStatus



from models.receta import Receta



class RecetaListResource(Resource):
    """ Responde a /smilecook """

    def get(self):
        """
        Respuesta al método GET,
        que retorna todas las recetas
        """
        datos = [ receta.data for receta in Receta.get_all() if receta.es_publicada ]

        return {"data": datos}, HTTPStatus.OK

    def post(self):
        """
        Respuesta ante el método http POST.
        Espera recibir los datos de una receta para
        guardarlos. Retorna la receta creada.
        """
        datos = request.get_json()

        nombre_receta = datos["nombre"]

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

        return {"data": receta.data}, HTTPStatus.CREATED



class RecetaResource(Resource):
    """ Responde a /smilecook/<receta_id> """
    def get(self, receta_id):
        receta = Receta.get_by_id(receta_id)
        if receta is None:
            return {'message': 'receta no encontrada'}, HTTPStatus.NOT_FOUND
        return {'data': receta.data}, HTTPStatus.OK

    def put (self, receta_id):
        receta = Receta.get_by_id(receta_id)

        if receta is None:
            return {'message': 'receta no encontrada'}, HTTPStatus.NOT_FOUND

        datos = request.get_json()
        receta.nombre = datos['nombre']
        receta.descripcion = datos['descripcion']
        receta.raciones = datos['raciones']
        receta.tiempo = datos['tiempo']
        receta.pasos = datos['pasos']

        receta.guardar()
        return {'data': receta.data}, HTTPStatus.OK



class RecetaPublishResource(Resource):
    """ Responde a /smilecook/<receta_id> """
    def patch(self, receta_id):
        receta = Receta.get_by_id(receta_id)
        if receta is None:
            return {'message': 'receta no encontrada'}, HTTPStatus.NOT_FOUND
        receta.es_publicada = True
        receta.guardar()
        return {}, HTTPStatus.NO_CONTENT

    def delete(self, receta_id):
        receta = Receta.get_by_id(receta_id)
        if receta is None:
            return {'message': 'receta no encontrada'}, HTTPStatus.NOT_FOUND
        receta.es_publicada = False
        receta.guardar()
        return {}, HTTPStatus.NO_CONTENT

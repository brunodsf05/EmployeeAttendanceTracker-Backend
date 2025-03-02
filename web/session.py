from flask import request, make_response
from flask_jwt_extended import decode_token, create_access_token, get_jwt_identity, exceptions



def is_authenticated():
    """ Verifica si el usuario está autenticado y renueva el token si es necesario """
    try:
        token = request.cookies.get("access_token")

        if token:
            decode_token(token)  # Verifica si el token es válido
            return True

    except exceptions.ExpiredSignatureError:
        # Si el token expiró, intentamos renovarlo con el refresh token
        refresh_token = request.cookies.get("refresh_token")

        if refresh_token:
            try:
                identity = decode_token(refresh_token)["sub"]  # Obtiene el usuario asociado al refresh token
                new_access_token = create_access_token(identity=identity)

                # Crear una respuesta con la nueva cookie
                response = make_response(True)
                response.set_cookie("access_token", new_access_token, httponly=True)
                return response

            except exceptions.JWTExtendedException:
                pass  # Si hay algún error con el refresh token, el usuario no está autenticado

    return False

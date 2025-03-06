from flask import request
from flask_jwt_extended import decode_token, exceptions



def is_authenticated():
    """ Verifica si el usuario está autenticado """
    try:
        token = request.cookies.get("access_token")

        if token:
            # Intenta decodificar el token (si es válido)
            decode_token(token)
            return True

    except exceptions.JWTExtendedException:
        # Si hay cualquier error con el token, consideramos que no está autenticado
        pass

    except Exception as e:
        pass

    return False



def get_authenticated_username():
    """ Recupera el username del usuario autenticado a partir del token """
    try:
        token = request.cookies.get("access_token")

        if token:
            decoded_token = decode_token(token)
            return decoded_token.get("sub")

    except exceptions.JWTExtendedException:
        pass

    except Exception:
        pass

    return None
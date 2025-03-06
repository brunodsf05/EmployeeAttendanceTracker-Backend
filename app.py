from flask import Flask, render_template, redirect, url_for, abort, make_response
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from http import HTTPStatus
from datetime import datetime
from mytime import MyTime

from config import Config
from extensions import db
from models import Dia, Empresa, FranjaHoraria, Horario, Incidencia, Receta, Registro, Rol, Trabajador
from resources import LoginResource, FichajeResource
from web import LoginForm, EmpresaForm, TrabajadorForm, MyTimeForm, is_authenticated, get_authenticated_username
from flask_jwt_extended import decode_token, create_access_token, create_refresh_token
from flask import request, redirect, url_for



# MARK: CONFIGURACIÓN

def  create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app



def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()



def register_resources(app):
    api = Api(app)
    api.add_resource(LoginResource, "/login")
    api.add_resource(FichajeResource, "/fichar")



app = create_app()
bootstrap = Bootstrap(app)



@app.context_processor
def inject_user():
    return dict(is_authenticated=is_authenticated, is_time_atomatic=MyTime.is_automatic)


# MARK: DEPURACIÓN

@app.shell_context_processor
def make_shell_contex():
    return dict(db=db, Dia=Dia, Empresa=Empresa, FranjaHoraria=FranjaHoraria, Horario=Horario, Incidencia=Incidencia, Receta=Receta, Registro=Registro, Rol=Rol, Trabajador=Trabajador)



# MARK: SESIÓN DE ADMINISTRADOR

def is_allowed_to_try_to_regain_session():
    """
    Verifica si se tiene la cookie de refresh_token y no se está autenticado.
    Así podemos evitar falsos errores 404 al intentar entrar a index o login por primera vez.
    """
    return request.cookies.get("refresh_token") and not is_authenticated()

def try_to_regain_session():
    """ 
    Intenta recuperar la sesión del administrador a partir del refresh_token en cookies.
    Si no puede, redirige a la página de error.
    """
    
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return abort(HTTPStatus.NOT_FOUND)

    try:
        # Decodificar el refresh_token y obtener la identidad
        decoded_token = decode_token(refresh_token)
        identity = decoded_token.get("sub")

        if not identity:
            return abort(HTTPStatus.NOT_FOUND)


        # Crear nuevos tokens
        new_access_token = create_access_token(identity=identity, fresh=False)
        new_refresh_token = create_refresh_token(identity=identity)

        # Crear la respuesta y actualizar las cookies
        response = redirect(url_for("admin_login"))
        response.set_cookie("access_token", new_access_token, httponly=True, samesite="Lax")
        response.set_cookie("refresh_token", new_refresh_token, httponly=True, samesite="Lax")

        return response

    except Exception as e:
        response = make_response("Sesión no encontrada", HTTPStatus.NOT_FOUND)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("admin_name")

        return response


# MARK: FRONTEND

@app.route("/", methods=["GET", "POST"])
def index():
    """ Raíz del sitio """
    if is_allowed_to_try_to_regain_session():
        return try_to_regain_session()

    return render_template("index.html")



@app.route("/admin", methods=["GET", "POST"])
def admin_home():
   """ Redirige a la página de inicio del administrador web """
   return redirect(url_for("index"))



@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(e):
   """ La url no existe en el sistema """
   return render_template("404.html"), HTTPStatus.NOT_FOUND



# MARK: FE: SESIÓN

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """ Inicio de sesión solo para administradores """

    if is_allowed_to_try_to_regain_session():
        return try_to_regain_session()

    form = LoginForm()

    def goto_login(error=""):
        return render_template("forms/login.html", form=form, error=error)

    if form.validate_on_submit():
        # Buscar al administrador
        username = form.username.data
        password = form.password.data
        user = Trabajador.get_by_username(username)
        
        # Validaciones
        if user is None:
            return goto_login("Usuario no encontrado")

        if user.rol.nombre != "Administrador":
            return goto_login("No tienes permisos de administrador")

        if not user.check_password(password):
            return goto_login("Contraseña incorrecta")

        # Crear token JWT
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        
        # Almacenarlo en una cookie
        response = redirect(url_for("index"))
        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)

        response.set_cookie("admin_name", user.nombre, httponly=True)

        return response
        
    return goto_login()



@app.route("/logout")
def close():
    """ Cerrar la sesión del panel de control eliminando la cookie """
    response = redirect(url_for("index"))
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("admin_name")
    return response



# MARK: FE: EMPESA

@app.route("/admin/empresa", methods=["GET", "POST"])
def admin_empresa():
    """ Interfaz para configurar los datos de la empresa """
    if not is_authenticated():
        return try_to_regain_session()

    form = EmpresaForm()

    def goto_empresa(error="", sucess=False):
        time = datetime.now().isoformat() if sucess else ""
        return render_template("forms/empresa.html", form=form, error=error, latest_time=time)

    # Manejar existencia de la empresa
    empresa = Empresa.get_first()

    if empresa is None:
        return goto_empresa(error="No hay ninguna empresa registrada")

    # ¿Leemos o actualizamos?
    if form.validate_on_submit():
        # Actualizar los datos de la empresa
        empresa.nombre = form.nombre.data
        empresa.latitud = form.latitud.data
        empresa.longitud = form.longitud.data
        empresa.radio = form.radio.data
        empresa.save()

        return goto_empresa(sucess=True)
    else:
        # Rellenar el formulario con los datos de la empresa
        form.nombre.data = empresa.nombre
        form.latitud.data = empresa.latitud
        form.longitud.data = empresa.longitud
        form.radio.data = empresa.radio

    return goto_empresa()



# MARK: FE: TIEMPO

@app.route("/admin/tiempo", methods=["GET", "POST"])
def admin_mytime():
    """ Interfaz para configurar la fecha y horas del servidor """
    if not is_authenticated():
        return try_to_regain_session()

    form = MyTimeForm()

    def goto_mytime(error="", sucess=False):
        time = datetime.now().isoformat() if sucess else ""
        return render_template("forms/mytime.html", form=form, error=error, latest_time=time)

    # ¿Leemos o actualizamos?
    if form.validate_on_submit():
        # Actualizar los datos de la empresa
        if form.use_now.data:
            MyTime.set(True)

        else:
            fecha = form.date.data
            hora = form.time.data
            MyTime.set(False, fecha, hora)

        return goto_mytime(sucess=True)
    else:
        # Rellenar el formulario con los datos de la empresa
        form.use_now.data = MyTime.is_automatic()
        form.date.data = MyTime.get().date()
        form.time.data = MyTime.get().time()

    return goto_mytime()



# MARK: FE: EMPLEADOS

@app.route("/admin/empleados", methods=["GET", "POST"])
def admin_listar_empleados():
    """ Interfaz para listar a los empleados """
    if not is_authenticated():
        return try_to_regain_session()

    empleados_activos = Trabajador.get_all_activos()
    empleados_debaja = Trabajador.get_all_debaja()

    return render_template("lists/list_empleados.html", empleados_activos=empleados_activos, empleados_debaja=empleados_debaja)



@app.route("/admin/empleado/editar/<int:id>", methods=["GET", "POST"])
def admin_editar_empleado(id):
    """ Interfaz para modificar a un empleado """
    if not is_authenticated():
        return try_to_regain_session()

    form = TrabajadorForm(password_required=False)

    def goto_editar(error="", sucess=False):
        time = datetime.now().isoformat() if sucess else ""
        return render_template("forms/edit_trabajador.html", form=form, error=error, latest_time=time, id=id)

    # Manejar existencia del empleado
    trabajador = Trabajador.get_by_id(id)

    if trabajador is None:
        return goto_editar(error="No hay ningún trabajador registrado con ese ID")

    # ¿Leemos o actualizamos?
    if form.validate_on_submit():
        # Actualizar los datos del trabajador
        trabajador.nif = form.nif.data
        trabajador.nombre = form.nombre.data
        trabajador.telefono = form.telefono.data
        trabajador.username = form.username.data

        if form.password.data != "":
            trabajador.password = form.password.data

        trabajador.save()

        return goto_editar(sucess=True)
    else:
        # Rellenar el formulario con los datos del trabajador
        form.nif.data = trabajador.nif
        form.nombre.data = trabajador.nombre
        form.telefono.data = trabajador.telefono
        form.username.data = trabajador.username

    return goto_editar()



@app.route("/admin/empleado/agregar", methods=["GET", "POST"])
def admin_agregar_empleado():
    """ Interfaz para añadir a un empleado """
    if not is_authenticated():
        return try_to_regain_session()

    form = TrabajadorForm(password_required=True)

    def goto_agregar(error="", sucess=False):
        time = datetime.now().isoformat() if sucess else ""
        return render_template("forms/add_trabajador.html", form=form, error=error, latest_time=time)

    if form.validate_on_submit():
        # Creamos al trabajador
        Trabajador(
            nif=form.nif.data,
            nombre=form.nombre.data,
            telefono=form.telefono.data,
            username=form.username.data,
            password=form.password.data,
            # Cutre 😎
            rol=Rol.query.filter_by(nombre="Empleado").first(),
            empresa=Empresa.get_first(),
            horario=Horario.get_all()[0]
        ).save()

        return goto_agregar(sucess=True)

    return goto_agregar()



@app.route("/admin/empleado/dar/baja/<int:id>", methods=["GET", "POST"])
def admin_dardebaja_empleado(id):
    """ Interfaz para dar de baja a un empleado """
    if not is_authenticated():
        return try_to_regain_session()

    trabajador = Trabajador.get_by_id(id)

    if trabajador is None:
        return abort(HTTPStatus.NOT_FOUND)


    if trabajador.username == get_authenticated_username():
        return abort(HTTPStatus.NOT_FOUND)


    trabajador.debaja = True
    trabajador.save()

    return redirect(url_for("admin_listar_empleados"))



@app.route("/admin/empleado/dar/alta/<int:id>", methods=["GET", "POST"])
def admin_dardealta_empleado(id):
    """ Interfaz para dar de alta a un empleado """
    if not is_authenticated():
        return try_to_regain_session()

    trabajador = Trabajador.get_by_id(id)

    if trabajador is None:
        return abort(HTTPStatus.NOT_FOUND)


    trabajador.debaja = False
    trabajador.save()

    return redirect(url_for("admin_listar_empleados"))



# MARK: ENTRYPOINT

if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from http import HTTPStatus
from datetime import datetime

from config import Config
from extensions import db
from models import Dia, Empresa, FranjaHoraria, Horario, Incidencia, Receta, Registro, Rol, Trabajador
from resources import LoginResource, FichajeResource
from web import LoginForm, EmpresaForm, TrabajadorForm, is_authenticated
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, decode_token, create_access_token, create_refresh_token
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
    return dict(is_authenticated=is_authenticated)


# MARK: DEPURACIÓN

@app.shell_context_processor
def make_shell_contex():
    return dict(db=db, Dia=Dia, Empresa=Empresa, FranjaHoraria=FranjaHoraria, Horario=Horario, Incidencia=Incidencia, Receta=Receta, Registro=Registro, Rol=Rol, Trabajador=Trabajador)



# MARK: SESIÓN DE ADMINISTRADOR

def try_to_regain_session():
    """ Intenta recuperar la sesión del administrador a partir de las cookies. Si no puede, te lanza a la página de error """
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        return redirect(url_for("page_not_found"))

    try:
        decoded_token = decode_token(refresh_token)
        identity = decoded_token['sub']
        new_access_token = create_access_token(identity=identity)
        new_refresh_token = create_refresh_token(identity=identity)

        response = redirect(url_for("index"))
        response.set_cookie("access_token", new_access_token, httponly=True)
        response.set_cookie("refresh_token", new_refresh_token, httponly=True)
        return response

    except Exception:
        pass

    return redirect(url_for("page_not_found"))

# MARK: FRONTEND

@app.route("/", methods=["GET", "POST"])
def index():
   """ Raíz del sitio """
   return render_template("index.html")



@app.route("/admin", methods=["GET", "POST"])
def admin_home():
   """ Redirige a la página de inicio del administrador web """
   return redirect(url_for("index"))



@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """ Inicio de sesión solo para administradores """
    form = LoginForm()

    def goto_login(error=""):
        return render_template("login.html", form=form, error=error)

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



@app.route("/admin/empresa", methods=["GET", "POST"])
def admin_empresa():
    """ Interfaz para configurar los datos de la empresa """
    if not is_authenticated():
        return try_to_regain_session()

    form = EmpresaForm()

    def goto_empresa(error="", sucess=False):
        time = datetime.now().isoformat() if sucess else ""
        return render_template("empresa.html", form=form, error=error, latest_time=time)

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



@app.route("/admin/empleados", methods=["GET", "POST"])
def admin_listar_empleados():
    """ Interfaz para listar a los empleados """
    if not is_authenticated():
        return try_to_regain_session()

    empleados_activos = Trabajador.get_all_activos()
    empleados_debaja = Trabajador.get_all_debaja()

    return render_template("list_empleados.html", empleados_activos=empleados_activos, empleados_debaja=empleados_debaja)



@app.route("/admin/empleado/editar/<int:id>", methods=["GET", "POST"])
def admin_editar_empleado(id):
    """ Interfaz para modificar a un empleado """
    if not is_authenticated():
        return try_to_regain_session()

    form = TrabajadorForm(password_required=False)

    def goto_editar(error="", sucess=False):
        time = datetime.now().isoformat() if sucess else ""
        return render_template("edit_trabajador.html", form=form, error=error, latest_time=time, id=id)

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
        return render_template("empresa.html", form=form, error=error, latest_time=time)

    if form.validate_on_submit():
        # Creamos al trabajador
        Trabajador(
            nif=form.nif.data,
            nombre=form.nombre.data,
            telefono=form.telefono.data,
            username=form.username.data,
            password=form.password.data,
            # Cutre 😎
            rol=Rol.query.filter_by(nombre="Trabajador").first(),
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
        return redirect(url_for("page_not_found"))

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
        return redirect(url_for("page_not_found"))

    trabajador.debaja = False
    trabajador.save()

    return redirect(url_for("admin_listar_empleados"))



@app.route("/logout")
def close():
    """ Cerrar la sesión del panel de control eliminando la cookie """
    response = redirect(url_for("index"))
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("admin_name")
    return response



@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(e):
   """ La url no existe en el sistema """
   return render_template("404.html"), HTTPStatus.NOT_FOUND



# MARK: ENTRYPOINT

if __name__ == "__main__":
    app.run()

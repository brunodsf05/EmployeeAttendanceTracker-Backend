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
from web import LoginForm, EmpresaForm, is_authenticated



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
    if not is_authenticated():
        return try_to_regain_session()

    """ Interfaz para configurar los datos de la empresa """
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

    return render_template('list_empleados.html', empleados=Trabajador.get_all())



@app.route("/admin/empleado/editar/<id>", methods=["GET", "POST"])
def admin_editar_empleado():
    """ Interfaz para modificar a un empleado """
    if not is_authenticated():
        return try_to_regain_session()

    return redirect(url_for("index"))



@app.route("/admin/empleado/<id>", methods=["GET", "POST"])
def admin_agregar_empleado():
    """ Interfaz para añadir a un empleado """
    if not is_authenticated():
        return try_to_regain_session()

    return redirect(url_for("index"))



@app.route("/admin/empleado/dardebaja/<id>", methods=["GET", "POST"])
def admin_dardebaja_empleado():
    """ Interfaz para dar de baja a un empleado """
    if not is_authenticated():
        return try_to_regain_session()

    return redirect(url_for("index"))



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

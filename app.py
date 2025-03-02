from flask import Flask, render_template
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from http import HTTPStatus

from config import Config
from extensions import db
from models import Dia, Empresa, FranjaHoraria, Horario, Incidencia, Receta, Registro, Rol, Trabajador
from resources import LoginResource, FichajeResource



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



# MARK: DEPURACIÓN

@app.shell_context_processor
def make_shell_contex():
    return dict(db=db, Dia=Dia, Empresa=Empresa, FranjaHoraria=FranjaHoraria, Horario=Horario, Incidencia=Incidencia, Receta=Receta, Registro=Registro, Rol=Rol, Trabajador=Trabajador)



# MARK: FRONTEND

@app.route("/", methods=['GET', 'POST'])
def index():
   """ Raíz del sitio """
   return render_template("index.html")



@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(e):
   """ La url no existe en el sistema """
   return render_template("404.html"), HTTPStatus.NOT_FOUND



# MARK: ENTRYPOINT

if __name__ == "__main__":
    app.run()

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from extensions import db
from models import Dia, Empresa, FranjaHoraria, Horario, Incidencia, Receta, Registro, Rol, Trabajador
from resources import LoginResource
#from resources.recursosRecetas import RecetaListResource, RecetaResource, RecetaPublishResource



def  create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app



def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)



def register_resources(app):
    api = Api(app)
    api.add_resource(LoginResource, "/login")
    """
    api.add_resource(RecetaListResource, "/smilecook")
    api.add_resource(RecetaResource, "/smilecook/<int:receta_id>")
    api.add_resource(RecetaPublishResource, "/smilecook/<int:receta_id>")
    """



app = create_app()



@app.shell_context_processor
def make_shell_contex():
    return dict(db=db, Dia=Dia, Empresa=Empresa, FranjaHoraria=FranjaHoraria, Horario=Horario, Incidencia=Incidencia, Receta=Receta, Registro=Registro, Rol=Rol, Trabajador=Trabajador)



@app.route("/")
def index():
    return "ControlDePresencia"

"""
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = data.get("user")
    password = data.get('password')

    if not user or not password:
        return jsonify({"success": False, "message": "Invalid credentials"}), 400

    # Simulación de autenticación
    if user == "admin" and password == "password123":
        return jsonify({"success": True, "token": "your_generated_token"}), 200
    else:
        return jsonify({"success": False, "message": "Authentication failed"}), 401
"""

if __name__ == "__main__":
    app.run()

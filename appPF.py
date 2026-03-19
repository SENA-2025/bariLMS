from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import config
from db.db_connect import createPsqlDb

# from logger import logger
import os

load_dotenv()
db = createPsqlDb()

print(db)

migrate = Migrate() # Define migrate globally as well

def create_app(test_config=None):
    appPF = Flask(__name__, template_folder="templates-Etapa-Productiva")

    entorno = os.getenv("FLASK_ENV", "development")
    appPF.config.from_object(config[entorno])

    if test_config:
        appPF.config.update(test_config)
        
    with appPF.app_context():
        # Import models first so SQLAlchemy knows they exist
        # from models import models 
        from EtapaProductiva.models import models
        from EtapaProductiva.routes.index import index
        appPF.register_blueprint(index)
        print(models.Person)
        
        
        # # Now import and register Blueprints
       
        # from routes.Personroutes import person_routes
        # from routes.ProductRoutes import product_routes

    #     appPF.register_blueprint(person_routes)
    #     appPF.register_blueprint(product_routes)
        
    # logger.info("Aplicacion iniciada en entorno: %s", entorno)

    # # ─── ERRORES ───────────────────────────────────────
    # @appPF.errorhandler(404)
    # def not_found(e):
    #     logger.warning("Pagina no encontrada: %s", str(e))
    #     return render_template("errors/404.html"), 404

    # @appPF.errorhandler(500)
    # def server_error(e):
    #     logger.error("Error interno del servidor: %s", str(e))
    #     db.session.rollback()
    #     return render_template("errors/500.html"), 500

    return appPF
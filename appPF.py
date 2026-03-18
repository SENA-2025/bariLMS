from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import config
# from logger import logger
import os

load_dotenv()

# Define db globally but do not link to app yet
# CAMBIAR LA DB
# db = SQLAlchemy()
migrate = Migrate() # Define migrate globally as well

def create_app(test_config=None):
    appPF = Flask(__name__, template_folder="templates-proyecto-formativo")

    entorno = os.getenv("FLASK_ENV", "development")
    appPF.config.from_object(config[entorno])

    if test_config:
        appPF.config.update(test_config)

    if not appPF.config.get("POSTGRES_DATABASE_URI"):
        raise ValueError("DATABASE_URL no está definida. Revisa tu archivo .env")
    if not appPF.config.get("SECRET_KEY"):
        raise ValueError("SECRET_KEY no está definida. Revisa tu archivo .env")

    # 1. Initialize extensions
    # db.init_app(appPF)
    # migrate.init_app(appPF, db) # Initialize migrate here

    # 2. ─── RUTAS & MODELS ─────────────────────────────────
    # We use the app_context to ensure models are loaded into the metadata
    with appPF.app_context():
        # Import models first so SQLAlchemy knows they exist
        # from models import models 
        
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
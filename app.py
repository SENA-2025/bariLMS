from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import config
from logger import logger
import os

load_dotenv()

# Define db y migrate globalmente, sin vincular a la app aún
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates")

    entorno = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config[entorno])

    if test_config:
        app.config.update(test_config)

    # En desarrollo/testing no exijimos DATABASE_URL (puede funcionar sin BD por ahora)
    if not app.config.get("SECRET_KEY"):
        raise ValueError("SECRET_KEY no está definida. Revisa tu archivo .env")

    # 1. Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # 2. ─── MODELOS & RUTAS ──────────────────────────────────
    with app.app_context():
        # Importar modelos primero para que SQLAlchemy los registre
        from models import models  # noqa: F401

        # Registrar Blueprints
        from routes.auth_routes import auth_routes
        from routes.dashboard_routes import dashboard_routes

        app.register_blueprint(auth_routes)
        app.register_blueprint(dashboard_routes)

    logger.info("Aplicación bariLMS iniciada en entorno: %s", entorno)

    # ─── ERRORES ────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        logger.warning("Página no encontrada: %s", str(e))
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.error("Error interno del servidor: %s", str(e))
        db.session.rollback()
        return render_template("errors/500.html"), 500

    return app

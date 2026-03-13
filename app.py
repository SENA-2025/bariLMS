from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import config
from logger import logger
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates")

    entorno = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config[entorno])

    if test_config:
        app.config.update(test_config)

    if not app.config.get("SECRET_KEY"):
        raise ValueError("SECRET_KEY no está definida. Revisa tu archivo .env")

    # Extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Importar modelos
        from models import models  # noqa: F401

        # Registrar Blueprints
        from routes.auth_routes import auth_routes
        from routes.dashboard_routes import dashboard_routes
        from routes.sena_routes import sena_routes
        from routes.formacion_routes import formacion_routes
        from routes.instructores_routes import instructores_routes
        from routes.fichas_routes import fichas_routes
        from routes.aprendices_routes import aprendices_routes

        app.register_blueprint(auth_routes)
        app.register_blueprint(dashboard_routes)
        app.register_blueprint(sena_routes)
        app.register_blueprint(formacion_routes)
        app.register_blueprint(instructores_routes)
        app.register_blueprint(fichas_routes)
        app.register_blueprint(aprendices_routes)

    # Context processor global: inyecta session_user en todos los templates
    @app.context_processor
    def inject_session_user():
        from flask import session as flask_session
        from services.auth_service import get_current_user
        return {
            "session_user": get_current_user(),
            "session_user_email": flask_session.get("user_email", ""),
        }

    logger.info("bariLMS iniciado en entorno: %s", entorno)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.error("Error 500: %s", str(e))
        db.session.rollback()
        return render_template("errors/500.html"), 500

    return app

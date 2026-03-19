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
        from models import models
        from routes.index import index
        appPF.register_blueprint(index)
        print(models.Person)
        
    return appPF
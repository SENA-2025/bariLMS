import os
from dotenv import load_dotenv

load_dotenv()

class psqldb:
    # Replace these placeholders with your actual DBngin credentials
    DB_HOST = "localhost" # DBngin often uses 'localhost' or '127.0.0.1'
    DB_NAME = "bari"
    DB_USER = "postgres"
    DB_PASSWORD = ""
    DB_PORT = "5450" # Check your specific port in DBngin
        

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    POSTGRES_DATABASE_URI = os.getenv("DATABASE_URL")


class ProductionConfig(Config):
    DEBUG = False
    POSTGRES_DATABASE_URI = os.getenv("DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SECRET_KEY = "clave-para-tests"
    POSTGRES_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

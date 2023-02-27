import os
from decouple import config
from datetime import timedelta

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY=config('SECRET_KEY', 'secret')
    SQLALCHEMY_TRACK_MODIFICATION=False
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_PRIVATE_KEY=config('JWT_PRIVATE_KEY')
    PROPAGATE_EXCEPTIONS = True

class DevConfig(Config):
    DEBUG=config('DEBUG', cast=bool)
    SQLALCHEMY_ECHO=True
    DATABASE=config('DATABASE')
    SQLALCHEMY_DATABASE_URI=f"postgresql+psycopg2://postgres:root@localhost:5432/{DATABASE}"

class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_ECHO=True
    TEST_DATABASE=config('TEST_DATABASE')
    SQLALCHEMY_DATABASE_URI= "sqlite://" 
    DEBUG=config('DEBUG', cast=bool)


class ProductionConfig(Config):
    pass


config_dict = {
    'dev': DevConfig,
    'prod': ProductionConfig,
    'test': TestConfig
}
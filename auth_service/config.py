import os 
from flask_sqlalchemy import SQLAlchemy

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://sebastian:7501095@localhost:5432/auth_db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()

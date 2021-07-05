from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import os
from dotenv import find_dotenv, load_dotenv
from flask_jwt_extended import JWTManager
load_dotenv(find_dotenv(".env"))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


from api.urls import *

if __name__ == '__main__':
    app.run()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv(".env"))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from api.urls import *

if __name__ == '__main__':
    app.run()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import os
from dotenv import find_dotenv, load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_rest_paginate import Pagination

load_dotenv(find_dotenv(".env"))


app = Flask(__name__)
cors = CORS(resources={
    r'/*': {
        'origins': [
            'http://localhost:3000'
        ]
    }
})

cors.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)
app.config['PAGINATE_PAGE_SIZE'] = 2
app.config['PAGINATE_PAGINATION_OBJECT_KEY'] = None
app.config['PAGINATE_DATA_OBJECT_KEY'] = 'results'

db = SQLAlchemy(app)

pagination = Pagination(app, db)

migrate = Migrate(app, db)

jwt = JWTManager(app)


from api.urls import *

if __name__ == '__main__':
    app.run()

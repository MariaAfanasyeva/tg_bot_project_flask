from flask_restful import Api
from .resources import *
from app import app

api = Api(app)

api.add_resource(CategoryListResource, '/categories')
api.add_resource(CategoryDetailResource, '/category/<int:id>')
api.add_resource(BotListOrCreateResource, '/bots')

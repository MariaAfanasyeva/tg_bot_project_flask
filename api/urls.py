from flask_restful import Api
from .resources import *
from app import app

api = Api(app)

api.add_resource(CategoryListResource, '/categories')
api.add_resource(CategoryDetailResource, '/category/<int:id>')
api.add_resource(BotListOrCreateResource, '/api', endpoint="bots")
api.add_resource(BotResource, '/api/detail/<int:id>', endpoint="detail")
api.add_resource(BotListOrCreateResource, '/api/create', endpoint="create")
api.add_resource(BotResource, '/api/update/<int:id>', endpoint="update")
api.add_resource(BotResource, '/api/delete/<int:id>', endpoint="delete")

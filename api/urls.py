from flask_restful import Api
from .resources import CategoryListResource, CategoryDetailResource, BotListOrCreateResource, BotResource, \
    SignUpUserResource, UserLoginResource, UsersListResource
from app import app

api = Api(app)

api.add_resource(CategoryListResource, '/api/category')
api.add_resource(CategoryDetailResource, '/category/<int:id>')
api.add_resource(BotListOrCreateResource, '/api/bots', endpoint="bots")
api.add_resource(BotResource, '/api/detail/<int:id>', endpoint="detail")
api.add_resource(BotListOrCreateResource, '/api/create', endpoint="create")
api.add_resource(BotResource, '/api/update/<int:id>', endpoint="update")
api.add_resource(BotResource, '/api/delete/<int:id>', endpoint="delete")
api.add_resource(SignUpUserResource, '/auth/users/', endpoint="user_register")
api.add_resource(UsersListResource, '/users', endpoint="users")
api.add_resource(UserLoginResource, '/api/token/', endpoint="create token")

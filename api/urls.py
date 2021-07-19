from flask_restful import Api

from app import app

from .resources import (BotListOrCreateResource, BotResource,
                        CategoryDetailResource, CategoryListResource,
                        CommentBotResource, CommentResource,
                        CommentsUserResource, SignUpUserResource,
                        UserLoginResource, UsersListResource)

api = Api(app)

api.add_resource(CategoryListResource, "/category")
api.add_resource(CategoryDetailResource, "/category/<int:id>/bots")
api.add_resource(BotListOrCreateResource, "/bots", endpoint="bots")
api.add_resource(BotResource, "/bot/<int:id>", endpoint="update")
api.add_resource(CommentBotResource, "/bot/<int:id>/comment", endpoint="bot_comments")
api.add_resource(
    CommentsUserResource, "/user/<int:id>/comment", endpoint="user_comments"
)
api.add_resource(CommentResource, "/comment/<int:id>", endpoint="comment")
api.add_resource(SignUpUserResource, "/auth/users", endpoint="user_register")
api.add_resource(UsersListResource, "/users", endpoint="users")
api.add_resource(UserLoginResource, "/token", endpoint="create token")

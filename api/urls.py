from flask_restful import Api

from app import app

from .resources import (
    AddLikeResource,
    BotListOrCreateResource,
    BotResource,
    BotsFromUserResource,
    CategoryDetailResource,
    CategoryListResource,
    CommentBotResource,
    CommentResource,
    CommentsUserResource,
    DeleteLikeResource,
    GetAllLikesResource,
    SignUpUserResource,
    UserLoginResource,
    UserResource,
    UsersListResource,
    VideoResource,
)

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
api.add_resource(AddLikeResource, "/bot/<int:id>/like", endpoint="like_to_bot")
api.add_resource(DeleteLikeResource, "/like/<int:id>", endpoint="delete_like")
api.add_resource(GetAllLikesResource, "/likes", endpoint="likes")
api.add_resource(VideoResource, "/video", endpoint="video")
api.add_resource(SignUpUserResource, "/auth/users", endpoint="user_register")
api.add_resource(UsersListResource, "/users", endpoint="users")
api.add_resource(UserResource, "/user/<int:id>/info", endpoint="user_info")
api.add_resource(BotsFromUserResource, "/user/<int:id>/bots", endpoint="user_bots")
api.add_resource(UserLoginResource, "/token", endpoint="create token")

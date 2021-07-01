from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import Category, User, Bot, Comment, Like


class CategorySchema(SQLAlchemySchema):
    class Meta:
        model = Category
        include_relationships = True
        load_instance = True

    id = auto_field()
    name = auto_field()


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    id = auto_field()
    username = auto_field()
    email = auto_field()
    password_hash = auto_field()
    is_admin = auto_field()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class BotSchema(SQLAlchemySchema):
    class Meta:
        model = Bot
        include_relationships = True
        load_instance = True

    id = auto_field()
    name = auto_field()
    description = auto_field()
    link = auto_field()
    author = auto_field()
    category_id = auto_field()
    add_by_user_id = auto_field()


bot_schema = BotSchema()
bots_schema = BotSchema(many=True)


class CommentSchema(SQLAlchemySchema):
    class Meta:
        model = Comment

    id = auto_field()
    to_bot_id = auto_field()
    author_id = auto_field()
    creation_date = auto_field()
    content = auto_field()


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


class LikeSchema(SQLAlchemySchema):
    class Meta:
        model = Like

    id = auto_field()
    to_bot_id = auto_field()
    author_id = auto_field()


like_schema = LikeSchema()
likes_schema = LikeSchema(many=True)

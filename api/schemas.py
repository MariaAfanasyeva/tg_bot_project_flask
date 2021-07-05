from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import Category, Bot, User


class CategorySchema(SQLAlchemySchema):
    class Meta:
        model = Category
        include_relationships = True
        load_instance = True

    id = auto_field()
    name = auto_field()


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


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


bot_schema = BotSchema()
bots_schema = BotSchema(many=True)


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    id = auto_field()
    username = auto_field()
    password = auto_field()
    email = auto_field()


user_schema = UserSchema()
users_schema = UserSchema(many=True)

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import Category, Bot


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

from marshmallow import Schema, fields


class BotSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    link = fields.Str()
    author = fields.Str()
    category_id = fields.Integer()


bot_schema = BotSchema()
bots_schema = BotSchema(many=True)


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str()


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str()
    password = fields.Str()
    email = fields.Email()


user_schema = UserSchema()
users_schema = UserSchema(many=True)

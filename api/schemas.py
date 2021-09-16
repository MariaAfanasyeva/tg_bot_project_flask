from marshmallow import Schema, fields


class BotSchema(Schema):
    id = fields.Integer(dump_only=True)
    create_time = fields.DateTime(dump_only=True)
    update_time = fields.DateTime(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    link = fields.Str()
    author = fields.Str()
    category_id = fields.Integer()
    add_by_user = fields.Integer()


bot_schema = BotSchema()
bots_schema = BotSchema(many=True)


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    create_time = fields.DateTime(dump_only=True)
    update_time = fields.DateTime(dump_only=True)
    name = fields.Str()


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    create_time = fields.DateTime(dump_only=True)
    update_time = fields.DateTime(dump_only=True)
    username = fields.Str()
    password = fields.Str()
    email = fields.Email()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class CommentSchema(Schema):
    id = fields.Integer(dump_only=True)
    create_time = fields.DateTime(dump_only=True)
    update_time = fields.DateTime(dump_only=True)
    to_bot = fields.Integer()
    add_by_user = fields.Integer()
    content = fields.Str()


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


class LikeSchema(Schema):
    id = fields.Integer(dump_only=True)
    create_time = fields.DateTime(dump_only=True)
    update_time = fields.DateTime(dump_only=True)
    to_bot_id = fields.Integer()
    add_by_user = fields.Integer()


like_schema = LikeSchema()
likes_schema = LikeSchema(many=True)


class VideoSchema(Schema):
    id = fields.Integer(dump_only=True)
    create_time = fields.DateTime(dump_only=True)
    update_time = fields.DateTime(dump_only=True)
    file_key = fields.Str()
    add_by_user = fields.Integer()
    s3_link = fields.Str()
    glacier_link = fields.Str()


video_schema = VideoSchema()
videos_schema = VideoSchema(many=True)

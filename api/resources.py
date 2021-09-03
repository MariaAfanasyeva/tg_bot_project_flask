from __future__ import absolute_import
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

import tasks
from app import db, pagination, s3

from .models import Bot, Category, Comment, Like, User, Video
from .schemas import (
    bot_schema,
    bots_schema,
    categories_schema,
    category_schema,
    comment_schema,
    comments_schema,
    like_schema,
    likes_schema,
    user_schema,
    users_schema,
)

S3_OBJECT_BASE_URL = "https://flask-video-tg.s3.eu-central-1.amazonaws.com/"


class UserLoginResource(Resource):
    def post(self):
        username = request.json["username"]
        password = request.json["password"]
        user = User.query.filter_by(username=username).first()
        if user:
            current_user_password = user.password
            if check_password_hash(current_user_password, password):
                access_token = create_access_token(identity=user.id)
                return jsonify({"access_token": access_token})
        return jsonify({"message": "Invalid credentials!"})


class CategoryListResource(Resource):
    def get(self):
        categories = Category.query.all()
        return categories_schema.dump(categories)

    def post(self):
        name = request.json["name"]
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return category_schema.dump(new_category)


class CategoryDetailResource(Resource):
    def get(self, id):
        bots = Bot.query.filter_by(category_id=id)
        return pagination.paginate(bots, bots_schema, marshmallow=True)


class BotListOrCreateResource(Resource):
    def get(self):
        if search_parameter := request.args.get("search"):
            bots = Bot.query.filter(
                or_(
                    Bot.name.ilike(f"%{search_parameter}%"),
                    Bot.author.ilike(f"%{search_parameter}%"),
                    Bot.description.ilike(f"%{search_parameter}%"),
                )
            )
        else:
            bots = Bot.query.all()
        return pagination.paginate(bots, bots_schema, marshmallow=True)

    @jwt_required()
    def post(self):
        name = request.json["name"]
        description = request.json["description"]
        link = request.json["link"]
        author = request.json["author"]
        category_id = request.json["category_id"]
        new_bot = Bot(
            name=name,
            description=description,
            link=link,
            author=author,
            category_id=category_id,
            add_by_user=get_jwt_identity(),
        )
        db.session.add(new_bot)
        db.session.commit()
        return bot_schema.dump(new_bot), 201


class BotResource(Resource):
    def get(self, id):
        bot = Bot.query.get_or_404(id)
        return bot_schema.dump(bot)

    @jwt_required()
    def put(self, id):
        bot = Bot.query.get_or_404(id)
        if bot.add_by_user == get_jwt_identity():
            bot.name = request.json["name"]
            bot.description = request.json["description"]
            bot.link = request.json["link"]
            bot.author = request.json["author"]
            bot.category_id = request.json["category_id"]
            db.session.commit()
            return bot_schema.dump(bot)
        else:
            return jsonify({"message": "Only authors can edit bots"})

    @jwt_required()
    def delete(self, id):
        bot = Bot.query.get_or_404(id)
        if bot.add_by_user == get_jwt_identity():
            db.session.delete(bot)
            db.session.commit()
            return "", 204
        else:
            return jsonify({"message": "Only authors can delete bots"})


class BotsFromUserResource(Resource):
    def get(self, id):
        bots = Bot.query.filter_by(add_by_user=id)
        return pagination.paginate(bots, bots_schema, marshmallow=True)


class CommentBotResource(Resource):
    @jwt_required()
    def post(self, id):
        to_bot = id
        content = request.json["content"]
        new_comment = Comment(
            to_bot_id=to_bot, add_by_user=get_jwt_identity(), content=content
        )
        db.session.add(new_comment)
        db.session.commit()
        return comment_schema.dump(new_comment), 201

    def get(self, id):
        comments = Comment.query.filter_by(to_bot_id=id)
        return pagination.paginate(comments, comments_schema, marshmallow=True)


class CommentsUserResource(Resource):
    def get(self, id):
        comments = Comment.query.filter_by(add_by_user=id)
        return pagination.paginate(comments, comments_schema, marshmallow=True)


class CommentResource(Resource):
    def get(self, id):
        comment = Comment.query.get_or_404(id)
        return comment_schema.dump(comment)

    @jwt_required()
    def put(self, id):
        comment = Comment.query.get_or_404(id)
        if comment.add_by_user == get_jwt_identity():
            comment.content = request.json["content"]
            db.session.commit()
            return comment_schema.dump(comment)
        else:
            return jsonify({"message": "Only authors can edit comments"})

    @jwt_required()
    def delete(self, id):
        comment = Comment.query.get_or_404(id)
        if comment.add_by_user == get_jwt_identity():
            db.session.delete(comment)
            db.session.commit()
            return "", 204
        else:
            return jsonify({"message": "Only authors can delete comments"})


class GetAllLikesResource(Resource):
    def get(self):
        likes = Like.query.all()
        return likes_schema.dump(likes)


class AddLikeResource(Resource):
    @jwt_required()
    def post(self, id):
        new_like = Like(to_bot_id=id, add_by_user=get_jwt_identity())
        db.session.add(new_like)
        db.session.commit()
        return like_schema.dump(new_like), 201


class DeleteLikeResource(Resource):
    @jwt_required()
    def delete(self, id):
        like = Like.query.get_or_404(id)
        if like.add_by_user == get_jwt_identity():
            db.session.delete(like)
            db.session.commit()
            return "", 204
        else:
            return jsonify({"message": "Only authors can delete comments"})


class VideoResource(Resource):
    @jwt_required()
    def post(self):
        if "file" not in request.files:
            return jsonify({"messsage": "No file part"})
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"message": "No selected file."})
        if file:
            for obj in s3.list_objects(Bucket="flask-video-tg")["Contents"]:
                print(obj)
                if obj["Key"] == file.filename:
                    return jsonify(
                        {"message": "File with the same name already exists."}
                    )
                else:
                    try:
                        s3.upload_fileobj(
                            Fileobj=file, Bucket="flask-video-tg", Key=file.filename
                        )
                    except Exception:
                        return jsonify(
                            {
                                "message": "The file could not be uploaded. Something went wrong."
                            }
                        )
                    finally:
                        s3_link = S3_OBJECT_BASE_URL + file.filename
                        new_video = Video(
                            file_key=file.filename,
                            add_by_user=get_jwt_identity(),
                            s3_link=s3_link,
                        )
                        db.session.add(new_video)
                        print(db.session)
                        db.session.commit()
                        tasks.resize_video.delay(file.filename)
            return jsonify({"message": "Thanks for your video"})


class SignUpUserResource(Resource):
    def post(self):
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]

        user_with_same_name = User.query.filter_by(username=username).first()
        if user_with_same_name:
            return jsonify({"username": "User with the same name are already exists"})

        user_with_same_email = User.query.filter_by(email=email).first()
        if user_with_same_email:
            return jsonify({"email": "User with the same email are already exists"})

        password_hash = generate_password_hash(password, method="sha256")
        new_user = User(username=username, email=email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)


class UsersListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)


class UserResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user_schema.dump(user)

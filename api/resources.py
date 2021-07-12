from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, pagination

from .models import Bot, Category, User
from .schemas import *


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
        return pagination.paginate(
            bots,
            bots_schema,
            marshmallow=True,
            pagination_schema_hook=lambda current_page, page_obj: {
                "count": page_obj.total
            },
        )


class BotListOrCreateResource(Resource):
    def get(self):
        if request.args.get("search"):
            search_parameter = request.args.get("search")
        else:
            search_parameter = ""
        return pagination.paginate(
            Bot.query.filter(
                or_(
                    Bot.name.ilike(f"%{search_parameter}%"),
                    Bot.author.ilike(f"%{search_parameter}%"),
                    Bot.description.ilike(f"%{search_parameter}%"),
                )
            ),
            bots_schema,
            marshmallow=True,
            pagination_schema_hook=lambda current_page, page_obj: {
                "count": page_obj.total
            },
        )

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
        )
        db.session.add(new_bot)
        db.session.commit()
        return bot_schema.dump(new_bot)


class BotResource(Resource):
    def get(self, id):
        bot = Bot.query.get_or_404(id)
        return bot_schema.dump(bot)

    @jwt_required()
    def put(self, id):
        bot = Bot.query.get_or_404(id)
        bot.name = request.json["name"]
        bot.description = request.json["description"]
        bot.link = request.json["link"]
        bot.author = request.json["author"]
        bot.category_id = request.json["category_id"]
        db.session.commit()
        return bot_schema.dump(bot)

    @jwt_required()
    def delete(self):
        bot = Bot.query.get_or_404(id)
        db.session.delete(bot)
        db.session.commit()
        return "", 204


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

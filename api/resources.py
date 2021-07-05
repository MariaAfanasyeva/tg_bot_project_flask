from .schemas import *
from .models import Category, Bot, User
from app import pagination
from flask_restful import Resource
from app import db
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required


pagination_schema = lambda current_page, page_obj: {
    "count": page_obj.total
}


class UserLoginResource(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        user = User.query.filter_by(username=username).first()
        if user:
            current_user_password = user.password
            if check_password_hash(current_user_password, password):
                access_token = create_access_token(identity=user.id)
                return jsonify({'access_token': access_token})
        return jsonify({'message': 'Invalid credentials!'})


class CategoryListResource(Resource):
    def get(self):
        return pagination.paginate(Category, categories_schema, True, pagination_schema_hook=pagination_schema)

    def post(self):
        name = request.json['name']
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return category_schema.dump(new_category)


class CategoryDetailResource(Resource):
    def get(self, id):
        category = Category.query.get_or_404(id)
        return category_schema.dump(category)


class BotListOrCreateResource(Resource):
    def get(self):
        return pagination.paginate(Bot, bots_schema, True, pagination_schema_hook=pagination_schema)

    @jwt_required()
    def post(self):
        name = request.json['name']
        description = request.json['description']
        link = request.json['link']
        author = request.json['author']
        category_id = request.json['category_id']
        new_bot = Bot(name=name,
                      description=description,
                      link=link,
                      author=author,
                      category_id=category_id)
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
        bot.name = request.json['name']
        bot.description = request.json['description']
        bot.link = request.json['link']
        bot.author = request.json['author']
        bot.category_id = request.json['category_id']
        db.session.commit()
        return bot_schema.dump(bot)

    @jwt_required()
    def delete(self):
        bot = Bot.query.get_or_404(id)
        db.session.delete(bot)
        db.session.commit()
        return '', 204


class SignUpUserResource(Resource):
    def post(self):
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        user_with_same_name = User.query.filter_by(username=username).first()
        if user_with_same_name:
            return jsonify({'username': 'User with the same name are already exists'})

        user_with_same_email = User.query.filter_by(email=email).first()
        if user_with_same_email:
            return jsonify({'email': 'User with the same email are already exists'})

        password_hash = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)


class UsersListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)


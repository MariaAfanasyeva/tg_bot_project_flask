from .schemas import *
from .models import Category, User, Bot, Comment, Like
from flask_restful import Resource
from app import db
from flask import request


class CategoryListResource(Resource):
    def get(self):
        categories = Category.query.all()
        return categories_schema.dump(categories)


class CategoryDetailResource(Resource):
    def get(self, id):
        category = Category.query.get_or_404(id)
        return category_schema.dump(category)


class BotListOrCreateResource(Resource):
    def get(self):
        bots = Bot.query.all()
        return bots_schema.dump(bots)

    def post(self):
        name = request.json['name']
        description = request.json['description']
        link = request.json['link']
        author = request.json['author']
        category_id = request.json['category_id']
        add_by_user_id = request.json['add_by_user_id']
        new_bot = Bot(name=name,
                      description=description,
                      link=link,
                      author=author,
                      category_id=category_id,
                      add_by_user_id=add_by_user_id)
        db.session.add(new_bot)
        db.session.commit()
        return bot_schema.dump(new_bot)

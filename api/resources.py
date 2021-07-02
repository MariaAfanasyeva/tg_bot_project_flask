from .schemas import *
from .models import Category, Bot
from flask_restful import Resource
from app import db
from flask import request


class CategoryListResource(Resource):
    def get(self):
        categories = Category.query.all()
        return categories_schema.dump(categories)

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
        bots = Bot.query.all()
        return bots_schema.dump(bots)

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

    def put(self, id):
        bot = Bot.query.get_or_404(id)
        bot.name = request.json['name']
        bot.description = request.json['description']
        bot.link = request.json['link']
        bot.author = request.json['author']
        bot.category_id = request.json['category_id']
        db.session.commit()
        return bot_schema.dump(bot)

    def delete(self):
        bot = Bot.query.get_or_404(id)
        db.session.delete(bot)
        db.session.commit()
        return '', 204

from app import db
from datetime import datetime


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bots = db.relationship('Bot', backref='category', lazy=True)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class User(db.Model):
    __tablename__ = 'resource_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    bots = db.relationship('Bot', backref='creator', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    likes = db.relationship('Like', backref='like author', lazy=True)

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return f"{self.username}"


class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete="CASCADE"), nullable=True, default=None)
    add_by_user_id = db.Column(db.Integer, db.ForeignKey('resource_user.id', ondelete="CASCADE"), nullable=True, default=None)
    comments = db.relationship('Comment', backref='commented bot', lazy=True)
    likes = db.relationship('Like', backref='liked bot', lazy=True)

    def __str__(self):
        return f"{self.name} by {self.author}"

    def __repr__(self):
        return f"{self.name} by {self.author}"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_bot_id = db.Column(db.Integer, db.ForeignKey('bot.id', ondelete="CASCADE"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('resource_user.id', ondelete="SET NULL"))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=True)
    content = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f"comment to bot {self.to_bot_id} by user {self.author_id}"

    def __repr__(self):
        return f"comment to bot {self.to_bot_id} by user {self.author_id}"


class Like(db.Model):
    __tablename__ = 'bot_like'

    id = db.Column(db.Integer, primary_key=True)
    to_bot_id = db.Column(db.Integer, db.ForeignKey('bot.id', ondelete="CASCADE"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('resource_user.id', ondelete="SET NULL"))

    def __str__(self):
        return f"like to bot {self.to_bot_id} by user {self.author_id}"

    def __repr__(self):
        return f"like to bot {self.to_bot_id} by user {self.author_id}"

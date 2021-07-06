from app import db
from sqlalchemy.sql import func


class BaseModel:
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, server_default=func.now())
    update_date = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


class Category(db.Model, BaseModel):
    name = db.Column(db.String(100), nullable=False)
    bots = db.relationship('Bot', backref='category', lazy=True)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Bot(db.Model, BaseModel):
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete="SET NULL"),
                            nullable=True,
                            default=None)

    def __str__(self):
        return f"{self.name} by {self.author}"

    def __repr__(self):
        return f"{self.name} by {self.author}"


class User(db.Model, BaseModel):
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return f"{self.username}"

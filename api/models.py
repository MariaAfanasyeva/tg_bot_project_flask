import datetime

from sqlalchemy.sql import func

from app import db


class BaseModel(db.Model):
    __abstract__ = True
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


class Category(BaseModel):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    bots = db.relationship("Bot", backref="category", lazy=True)
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Bot(BaseModel):
    __tablename__ = "bot"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"{self.name} by {self.author}"

    def __repr__(self):
        return f"{self.name} by {self.author}"


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return f"{self.username}"

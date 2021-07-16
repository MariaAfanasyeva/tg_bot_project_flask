import datetime

from sqlalchemy.sql import func
from sqlalchemy_logger import Logger

from app import app, db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


class Category(BaseModel):
    __tablename__ = "category"
    bots = db.relationship("Bot", backref="category", lazy=True)
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Bot(BaseModel):
    __tablename__ = "bot"
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", ondelete="SET NULL"),
        nullable=True,
    )
    name = db.Column(db.String(100), nullable=False)
    add_by_user = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )

    def __str__(self):
        return f"{self.name} by {self.author}"

    def __repr__(self):
        return f"{self.name} by {self.author}"


class User(BaseModel):
    __tablename__ = "user"
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return f"{self.username}"


logger = Logger(app)

logger.listen_before_flush()
logger.listen_after_flush()
logger.listen_after_rollback()

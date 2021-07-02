from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bots = db.relationship('Bot', backref='category', lazy=True)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete="CASCADE"),
                            nullable=True,
                            default=None)

    def __str__(self):
        return f"{self.name} by {self.author}"

    def __repr__(self):
        return f"{self.name} by {self.author}"

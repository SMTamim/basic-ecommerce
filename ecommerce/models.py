from datetime import datetime
from ecommerce import db


# MODELS
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    price = db.Column(db.String(10), nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    color = db.Column(db.String(255), nullable=False)
    brandName = db.Column(db.String(255), nullable=False)
    size = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(5000), nullable=True)
    rating = db.Column(db.Integer, nullable=False, default=0)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    reviews = db.relationship('Reviews', backref='product', lazy=True)

    def __repr__(self):
        return f'Product(id:{self.id} Name:{self.name} Price:{self.price})'


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String(300), nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_id = db.relationship('Product', backref='category', lazy=True)
    name = db.Column(db.String(255), nullable=False, default="Uncategorized")
    tags = db.String(db.Text)

    def __repr__(self):
        return f'Category(id:{self.id} Name:{self.name} Tags:{self.tags})'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    access_level = db.Column(db.Integer, db.ForeignKey('accesslevel.id'), nullable=False)


class Accesslevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

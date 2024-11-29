from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# ユーザーモデル
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(3), nullable=False)

# 食材モデル
class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)

# 選択された食材モデル
class SelectedIngredient(db.Model):
    __tablename__ = 'selected_ingredient'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True, nullable=False)

    ingredient = db.relationship('Ingredient', backref='selected_ingredients', lazy=True)
    user = db.relationship('User', backref='selected_ingredients', lazy=True)

# レシピモデル
class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_name = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_favorite = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='recipes', lazy=True)
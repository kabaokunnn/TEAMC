from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
 
db = SQLAlchemy()
 
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(3), nullable=False)
 
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
 
class SelectedIngredient(db.Model):
    # 主キーとして `id` を使用するか、別の名前を使うことを検討
    id = db.Column(db.Integer, primary_key=True)  # 主キーを `id` に戻す
   
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   
    # `ingredient_id` を外部キーに使用
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    
    # リレーション設定はそのままで問題ありません
    ingredient = db.relationship('Ingredient', backref='selected_ingredients', lazy=True)
    user = db.relationship('User', backref='selected_ingredients', lazy=True)

# 必須属性を追加
@property
def is_active(self):
    # 常に有効とする場合は True を返す
    return True
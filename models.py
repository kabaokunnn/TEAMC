from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(3), nullable=False)
 
    # 必須属性を追加
    @property
    def is_active(self):
        # 常に有効とする場合は True を返す
        return True
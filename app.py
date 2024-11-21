from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from views import views
from models import db
 
# Flask アプリケーションの設定
app = Flask(__name__)
app.secret_key = 'your_secret_key'
 
# MySQL データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://0623:0623@localhost/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# 初期化
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'views.login'
 
# ユーザーローダーの設定
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
 
# ブループリントの登録
app.register_blueprint(views)
 
# データベーステーブルの作成
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created")
    app.run(debug=True)
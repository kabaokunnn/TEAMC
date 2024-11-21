from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
 
# Flask Blueprint 定義
views = Blueprint('views', __name__)
 
# ホームページ (ログイン必須)
@views.route('/')
@login_required
def home():
    return render_template('index.html', username=current_user.username)
 
# 新規登録
@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # フォームからデータを取得
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
 
        # ユーザー名またはメールアドレスの重複チェック
        if User.query.filter_by(username=username).first():
            flash('このユーザー名は既に登録されています。', 'danger')
            return redirect(url_for('views.register'))
        if User.query.filter_by(email=email).first():
            flash('このメールアドレスは既に登録されています。', 'danger')
            return redirect(url_for('views.register'))
 
        # パスワードをハッシュ化して保存 (pbkdf2:sha256)
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password, age=age, gender=gender)
        db.session.add(new_user)
        db.session.commit()
 
        flash('登録が成功しました！ログインしてください。', 'success')
        return redirect(url_for('views.login'))
 
    return render_template('register.html')
 
# ログイン
@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # フォームからデータを取得
        email = request.form['email']
        password = request.form['password']
 
        # ユーザーを取得
        user = User.query.filter_by(email=email).first()
 
        # パスワードの検証
        if user and user.password and check_password_hash(user.password, password):
            login_user(user)
            flash('ログインに成功しました！', 'success')
            return redirect(url_for('views.home'))
        else:
            flash('メールアドレスまたはパスワードが間違っています。', 'danger')
 
    return render_template('login.html')
 
# ログアウト
@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。', 'success')
    return redirect(url_for('views.login'))
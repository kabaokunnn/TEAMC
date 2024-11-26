from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Ingredient, SelectedIngredient

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

# 食材登録ページ
@views.route('/syokuzai', methods=['GET', 'POST'])
@login_required
def syokuzai():
    if request.method == 'POST':
        # POSTデータの処理
        selected_ingredients = request.form.getlist('ingredients')

        # 選択された食材をデータベースに保存
        for ingredient_id in selected_ingredients:
            ingredient = Ingredient.query.get(ingredient_id)
            if ingredient:
                selected_ingredient = SelectedIngredient(user_id=current_user.id, ingredient_id=ingredient.id)
                db.session.add(selected_ingredient)
        db.session.commit()

        flash('選択された食材を保存しました！', 'success')
        return redirect(url_for('views.list_syokuzai'))  # 登録後に list_syokuzai.html に遷移

    # データベースから食材データを取得
    beef = Ingredient.query.filter_by(category="牛肉").all()
    pork = Ingredient.query.filter_by(category="豚肉").all()
    chicken = Ingredient.query.filter_by(category="鶏肉").all()
    other_meat = Ingredient.query.filter_by(category="その他の肉").all()
    vegetables = Ingredient.query.filter_by(category="野菜").all()
    mushrooms = Ingredient.query.filter_by(category="きのこ").all()
    seafood = Ingredient.query.filter_by(category="魚介").all()
    eggs_dairy = Ingredient.query.filter_by(category="卵・乳製品").all()
    beans_tubers = Ingredient.query.filter_by(category="豆・芋").all()
    grains_bread = Ingredient.query.filter_by(category="米・穀・パン").all()
    fruits = Ingredient.query.filter_by(category="果物").all()
    other = Ingredient.query.filter_by(category="その他").all()

    # データをテンプレートに渡す
    return render_template(
        'syokuzai.html',
        beef=beef,
        pork=pork,
        chicken=chicken,
        other_meat=other_meat,
        vegetables=vegetables,
        mushrooms=mushrooms,
        seafood=seafood,
        eggs_dairy=eggs_dairy,
        beans_tubers=beans_tubers,
        grains_bread=grains_bread,
        fruits=fruits,
        other=other
    )

# 登録完了ページ
@views.route('/confirmation')
@login_required
def confirmation():
    return render_template('confirmation.html')

# 食材一覧ページ (登録した食材を表示)
@views.route('/list_syokuzai', methods=['GET', 'POST'])
@login_required
def list_syokuzai():
    # ユーザーが選んだ食材を取得
    selected_ingredients = SelectedIngredient.query.filter_by(user_id=current_user.id).all()
    return render_template('list_syokuzai.html', selected_ingredients=selected_ingredients)

@views.route('/recipe', methods=['GET', 'POST'])
@login_required
def recipe():
    if request.method == 'POST':
        selected_items = request.form.getlist('selected_items')  # チェックボックスで選択された食材ID

        # 既存の選択食材を削除（必要な場合）
        SelectedIngredient.query.filter_by(user_id=current_user.id).delete()

        # 新たに選択された食材を保存
        for item_id in selected_items:
            selected_ingredient = SelectedIngredient(user_id=current_user.id, ingredient_id=item_id)
            db.session.add(selected_ingredient)

        # 保存処理を確定
        db.session.commit()

        # 保存後に「食材選択」画面にリダイレクト（または他の適切なページ）
        return redirect(url_for('views.recipe'))  # ここをリダイレクト先に変更

    # GETリクエスト時には食材選択フォームを表示
    selected_ingredients = SelectedIngredient.query.filter_by(user_id=current_user.id).all()
    return render_template('recipe.html', selected_ingredients=selected_ingredients)

# ログアウト
@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。', 'success')
    return redirect(url_for('views.login'))
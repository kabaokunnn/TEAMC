import google.generativeai as genai
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Ingredient, SelectedIngredient

views = Blueprint('views', __name__)

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

@views.route('/syokuzai', methods=['GET', 'POST'])
@login_required
def syokuzai():
    if request.method == 'POST':
        selected_ingredients = request.form.getlist('ingredients')

        for ingredient_id in selected_ingredients:
            if not ingredient_id.strip():  # 空値のチェック
                continue

            try:
                ingredient_id = int(ingredient_id)
            except ValueError:
                flash(f"無効な食材ID: {ingredient_id}", "danger")
                return redirect(url_for('views.syokuzai'))

            ingredient = Ingredient.query.get(ingredient_id)
            if not ingredient:
                flash(f"食材が見つかりません: ID {ingredient_id}", "danger")
                continue

            existing_entry = SelectedIngredient.query.filter_by(
                user_id=current_user.id,
                ingredient_id=ingredient.id
            ).first()

            if not existing_entry:
                new_entry = SelectedIngredient(user_id=current_user.id, ingredient_id=ingredient.id)
                db.session.add(new_entry)

        db.session.commit()
        flash('選択された食材を保存しました！', 'success')
        return redirect(url_for('views.list_syokuzai'))

    categories = {
        "牛肉": Ingredient.query.filter_by(category="牛肉").all(),
        "豚肉": Ingredient.query.filter_by(category="豚肉").all(),
        "鶏肉": Ingredient.query.filter_by(category="鶏肉").all(),  
        "野菜": Ingredient.query.filter_by(category="野菜").all(),
        "果物": Ingredient.query.filter_by(category="果物").all(),
        "その他の肉": Ingredient.query.filter_by(category="その他の肉").all(),
        "きのこ": Ingredient.query.filter_by(category="きのこ").all(),
        "魚介": Ingredient.query.filter_by(category="魚介").all(),
        "卵・乳製品": Ingredient.query.filter_by(category="卵・乳製品").all(),
        "豆・芋": Ingredient.query.filter_by(category="豆・芋").all(),
        "米・穀・パン": Ingredient.query.filter_by(category="米・穀・パン").all(),
        "その他": Ingredient.query.filter_by(category="その他").all(),
    }

    return render_template('syokuzai.html', categories=categories)

@views.route('/list_syokuzai', methods=['GET'])
@login_required
def list_syokuzai():
    selected_ingredients = SelectedIngredient.query.filter_by(user_id=current_user.id).all()
    return render_template('list_syokuzai.html', selected_ingredients=selected_ingredients)

@views.route('/delete_ingredient/<int:ingredient_id>', methods=['POST'])
@login_required
def delete_ingredient(ingredient_id):
    selected_ingredient = SelectedIngredient.query.filter_by(user_id=current_user.id, ingredient_id=ingredient_id).first()
    if selected_ingredient:
        db.session.delete(selected_ingredient)
        db.session.commit()
        flash('食材を削除しました！', 'success')
    else:
        flash('食材が見つかりませんでした。', 'danger')
    return redirect(url_for('views.list_syokuzai'))

@views.route('/recipe', methods=['GET', 'POST'])
@login_required
def recipe():
    if request.method == 'POST':
        selected_items = request.form.getlist('selected_items')

        if not selected_items:
            flash('食材を選択してください。', 'danger')
            return redirect(url_for('views.recipe'))

        # 提案画面に選択済み食材を渡す
        return redirect(url_for('views.teian'))

    selected_ingredients = SelectedIngredient.query.filter_by(user_id=current_user.id).all()
    return render_template('recipe.html', selected_ingredients=selected_ingredients)

# @views.route('/propose_recipe', methods=['GET'])
# @login_required
# def propose_recipe():
#     # レシピ提案のロジック（仮）
#     flash('レシピ提案画面へようこそ！', 'success')
#     return render_template('propose_recipe.html')

# Geminiにリクエストを送信する関数
# Geminiにリクエストを送信する関数
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
 
# 食材リストを受け取ってGemini APIを使ってレシピを生成
def get_recipe_from_gemini(ingredients_list):
    prompt = f"以下の食材を使ったレシピを提案してください: {', '.join(ingredients_list)}"
    gemini_pro = genai.GenerativeModel("gemini-pro")
    response = gemini_pro.generate_content(prompt)
   
    if response.text:
        return response.text
    else:
        return "レシピの生成に失敗しました。"
 
 
# /teianルートの追加
@views.route('/teian', methods=['POST'])
@login_required
def teian():
    selected_items = request.form.getlist('selected_items')  # チェックボックスで選択された食材IDのリストを取得
 
    # 選択された食材をDBから取得
    selected_ingredients = Ingredient.query.filter(Ingredient.id.in_(selected_items)).all()
 
    # 食材名のリストを作成
    ingredient_names = [ingredient.name for ingredient in selected_ingredients]
 
    # Gemini APIを使ってレシピを生成
    recipe_suggestions = get_recipe_from_gemini(ingredient_names)
 
    # レシピ提案をテンプレートに渡す
    return render_template('teian.html', recipe_suggestions=recipe_suggestions)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。', 'success')
    return redirect(url_for('views.login'))

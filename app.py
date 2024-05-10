from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__, template_folder='news_portal/templates', static_folder='news_portal/static')
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = 'NRIVIUBIUguirgnuirngurty44844t48rugfnfbf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Category('{self.name}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)  # Добавлено поле для связи с категорией

    # Связь с моделью Category
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    # Добавляем внешний ключ и связь с пользователем
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f"Comment('{self.body}', '{self.date_posted}')"


class CommentForm(FlaskForm):
    body = TextAreaField('Your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')


# @app.route('/')
# def index():
#     posts = Post.query.all()
#     category = Category.query.all()
#     return render_template('index.html', posts=posts, category=category)

@app.route('/')
def index():
    category_id = request.args.get('category_id')  # Получаем ID категории из запроса, если он есть
    posts = Post.query.all()
    categories = Category.query.all()

    if category_id:  # Если указан ID категории, фильтруем посты
        posts = Post.query.filter_by(category_id=category_id).all()

    return render_template('index.html', posts=posts, categories=categories, title='Главная')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post_id=post.id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('post_detail', post_id=post.id))
    comments = Comment.query.filter_by(post_id=post.id).order_by(desc(Comment.date_posted)).all()
    return render_template('post_detail.html', post=post, form=form, comments=comments, title='Новость')


@app.route('/about/')
def about():
    return render_template('about.html', title='О нас')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Если пользователь уже аутентифицирован, перенаправляем его
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Здесь нужно реализовать вашу логику аутентификации
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            next_page = request.args.get('next')  # Переход на следующую страницу, если был предоставлен параметр next
            return redirect(next_page or url_for('index'))
        else:
            return 'Invalid username or password'

    return render_template('login.html', title='Вход')


@login_manager.user_loader
def load_user(user_id):
    # Загрузка пользователя из базы данных или другого источника данных по ID
    return User.query.get(int(user_id))


login_manager.init_app(app)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


admin = Admin(app)


class PostAdminView(ModelView):
    column_list = ('id', 'title', 'content', 'date_posted', 'category', 'user_id', 'author')  # Заменили category_id и user_id на category и user
    column_searchable_list = ['title']


# Зарегистрированные модели с административным интерфейсом
admin.add_view(ModelView(User, db.session))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Category, db.session))


if __name__ == '__main__':
    app.run(debug=True)


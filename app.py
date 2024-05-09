from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__, template_folder='news_portal/templates', static_folder='news_portal/static')
app.config['SECRET_KEY'] = 'NRIVIUBIUguirgnuirngurty44844t48rugfnfbf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


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


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/posts/<category_name>')
def posts_by_category(category_name):
    category = Category.query.filter_by(name=category_name).first()
    if category:
        category_posts = category.posts
        return render_template('posts.html', posts=category_posts, category=category)
    else:
        return "Категория не найдена", 404


admin = Admin(app)

# Зарегистрированные модели с административным интерфейсом
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Category, db.session))


if __name__ == '__main__':
    app.run(debug=True)


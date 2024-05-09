from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='news_portal/templates', static_folder='news_portal/static')
# app.config['SECRET_KEY'] = 'hard to guess'
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)


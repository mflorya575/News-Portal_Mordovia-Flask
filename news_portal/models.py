# from flask_sqlalchemy import SQLAlchemy
#
# # Импортируем объект app из вашего run.py, чтобы использовать его для настройки базы данных
# from run import app
#
#
# # Определяем модель пользователя
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#
#     def __repr__(self):
#         return '<User %r>' % self.username

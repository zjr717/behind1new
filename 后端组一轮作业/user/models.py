from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User_bg(db.Model):
    __tablename__ = 'user_bg'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, plain_password):
        return check_password_hash(self.password_hash, plain_password)

    def __repr__(self):
        return f'<User {self.username}>'
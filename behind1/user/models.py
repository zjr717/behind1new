from flask_bcrypt import generate_password_hash, check_password_hash
from behind1.database import db


class User_bg(db.Model):
    __tablename__ = 'user_bg'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    username = db.Column(db.String(255), primary_key=True)
    password_hash = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, plain_password):
        return check_password_hash(self.password_hash, plain_password)

    def __repr__(self):
        return f'<User {self.username}>'
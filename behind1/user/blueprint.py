from flask import Blueprint
from behind1.database import db

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
db.init_app(user_bp)

from behind1.user import views

config = [
    (views.user_bp, '/')
]

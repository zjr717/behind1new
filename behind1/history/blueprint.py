from flask import Blueprint
from behind1.history import views

user_blueprint = Blueprint('user', __name__, url_prefix='/search')
config = [
    (views.history_bp, '/')
]

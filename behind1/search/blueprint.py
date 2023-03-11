from flask import Blueprint
from behind1.search import views

user_blueprint = Blueprint('user', __name__, url_prefix='/search')
config = [
    (views.search_bp, '/')
]

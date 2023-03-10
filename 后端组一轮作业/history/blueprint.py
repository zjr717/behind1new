from flask import Blueprint
from 后端组一轮作业.history import views

user_blueprint = Blueprint('user', __name__, url_prefix='/search')
config = [
    (views.history_bp, '/')
]

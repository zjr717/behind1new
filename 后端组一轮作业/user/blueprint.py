from flask import Blueprint
from 后端组一轮作业.user import views

user_blueprint = Blueprint('user', __name__, url_prefix='/user')
config = [
    (views.user_bp, '/')
]

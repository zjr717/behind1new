from flask import request, Blueprint, jsonify
import jwt
import time
from 后端组一轮作业.database import db
from .models import User_bg

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    check_password = data.get('checkPassword')

    if not all([username, password, check_password]):
        return jsonify(code=403, message='账号或密码为空！')

    if password != check_password:
        return jsonify(code=403, message='前后两次输入密码不一致！')

    user = User_bg(username=username, password=password)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(code=500, message='注册失败！', data={'error': str(e)})

    return jsonify(code=200, message='success', data={'id': user.id, 'username': user.username})


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify(code=403, message='账号或密码为空！')

    user = User_bg.query.filter_by(username=username).first()
    if user and user.check_password(password):
        payload = {'name': username, 'exp': int(time.time()) + 36000}
        token = jwt.encode(payload, 'secret_key', algorithm='HS256').decode('utf-8')
        return jsonify(code=200, message='success', data={'username': username, 'token': token})
    else:
        return jsonify(code=403, message='登录失败！请检查账号或密码是否正确。')
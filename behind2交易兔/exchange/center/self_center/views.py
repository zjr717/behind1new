from flask import render_template, Blueprint, current_app, request
from .models import db, User

# 创建一个蓝图对象，在主程序中导入并注册
bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/<int:user_id>')
def profile(user_id):
    # 根据用户id查询用户信息
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return '用户不存在'
    return render_template('profile.html', user=user)
from flask import render_template, Blueprint, current_app, request
from .models import db, Buyer

# 创建一个蓝图对象，在主程序中导入并注册
bp = Blueprint('buyer', __name__, url_prefix='/buyer')


@bp.route('/<int:buyer_id>')
def buyer_info(buyer_id):
    # 根据用户id查询用户信息
    buyer = Buyer.query.filter_by(id=buyer_id).first()
    if not buyer:
        return '用户不存在'
    return render_template('Buyer_center.html', user=buyer)
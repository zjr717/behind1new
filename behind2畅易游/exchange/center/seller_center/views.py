from flask import render_template, Blueprint, current_app, request
from .models import db, Seller

# 创建一个蓝图对象，在主程序中导入并注册
bp = Blueprint('seller', __name__, url_prefix='/seller')


@bp.route('/<int:seller_id>')
def seller_info(seller_id):
    # 根据用户id查询用户信息
    seller = Seller.query.filter_by(id=seller_id).first()
    if not seller:
        return '用户不存在'
    return render_template('seller_center.html', user=seller)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Buyer(db.Model):
    """
    买家表
    """
    __tablename__ = "Buyer"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 买家编号：买家的唯一标识符，通常为数字或字符串。
    name = db.Column(db.String(50), nullable=False)  # 买家名称：买家的名称或描述，可以是文字、图片等。
    order_count = db.Column(db.Integer, nullable=False)  # 订单数量：买家成功下单的数量，通常为数字。
    total_spend = db.Column(db.Float, nullable=False)  # 总消费金额：买家在平台上的总消费金额，通常为数字。
    average_order_value = db.Column(db.Float, nullable=False)  # 平均订单价值：买家每个订单的平均价值，通常为数字。
    favorite_category = db.Column(db.String(50), nullable=True)  # 偏好分类：买家喜欢购买的商品分类，可以是文字、图片等。
    last_purchase_date = db.Column(db.Date, nullable=True)  # 最后购买日期：买家最后一次购买的日期，通常为日期类型。
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Seller(db.Model):
    """
    卖家表
    """
    __tablename__ = "Seller"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 卖家编号：卖家的唯一标识符，通常为数字或字符串。
    name = db.Column(db.String(50), nullable=False)  # 卖家名称：卖家的名称或描述，可以是文字、图片等。
    merchandise_count = db.Column(db.Integer, nullable=False)  # 出售商品数量：出售商品的数量，通常为数字。
    total_sales = db.Column(db.Integer, nullable=False)  # 出售商品总销量：出售商品的销售数量，通常为数字。
    month_sales = db.Column(db.Integer, nullable=False)  # 本月出售商品销量：本月出售商品的销售数量，通常为数字。
    year_sales = db.Column(db.Integer, nullable=False)  # 本年出售商品销量：本年出售商品的销售数量，通常为数字。
    average_price = db.Column(db.Float, nullable=False)  # 出售商品平均价格：出售商品的平均价格，通常为数字。
    highest_bid = db.Column(db.Float, nullable=False)  # 最高出价：最高出价，通常为数字。
    completed_orders = db.Column(db.Integer, nullable=False)  # 已完成订单数：已完成的订单数量，通常为数字。


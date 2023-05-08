from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    '''
    用户表
    '''
    __tablename__ = "User"
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)  # 序号：内容非空,不重复,自增,主键
    username = db.Column(db.String(15), nullable=False, unique=True)  # 用户名：内容非空
    hash_password = db.Column(db.String(511), nullable=True)  # 密码：内容可空
    email = db.Column(db.String(31),nullable=True)  # 邮箱：内容可为空
    phone_number = db.Column(db.Integer,nullable=True )  # 手机号：内容可为空
    real_name = db.Column(db.String(50),nullable=True) # 真实姓名:内容可为空
    register_time = db.Column(db.DateTime,default=datetime.now())  # 注册时间:默认为当前时间
    last_time = db.Column(db.DateTime,default=datetime.now(), onupdate=datetime.now())  # 上次登录时间:默认为当前时间，更新时自动设置为当前时间
    profile_image= db.Column(db.String(15))  # 头像（应该是图片地址）：内容可为空

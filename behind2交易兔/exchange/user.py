from flask import redirect,jsonify,render_template,request,Flask,url_for
import sys
sys.path.append('/path/to/PyJWT')
# import jwt,PyJWT  # 安装PyJWT库，可以通过 pip install PyJWT 命令来安装。
import mysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from flask import Blueprint
# music
import prettytable as pt  # 取别名
import requests

from werkzeug.security import check_password_hash
# 文件
import util
from mysql import User
# import user
from mysql import app,db

import time # 获取当前时间
from datetime import datetime

# 蓝图
user = Blueprint('user', __name__)

# 登录
@user.route('/user/login',methods=['GET','POST'])
def login( ):
    # post表单数据时，处理数据，以下是处理数据
    info = request.get_json()  # 获取json数据
    # print(request.json)   # json和get_json一模一样
    # print(info)
    # get url参数时
    # username = request.args.get('username')
    get_username = info.get('username')
    get_password = str(info.get('password'))  # 拿到的是password不是hash_password
    hash_password = util.hash(get_password)  # 将get到的密码hash处理

    # 在数据库中通过username查找user
    user = User.query.filter_by(username=get_username).first()  # 这里的filter_by方法会返回一个查询对象，使用first方法可以获取查询结果中的第一条数据，即符合条件的用户数据。
    # user=User.query.get(1)
    # print(User.query.filter_by(username=get_username).all())

    # print(get_username)
    # print(get_password)
    # print(user)
    # print(hash_password)

    # 检验并返回查询结果
    if (user == None):  # 查询是否存在用户信息（username）
        return jsonify({"code":401,"msg":"用户名不存在"})
    else:  # 用户信息存在
        store_id = user.id  # 查询到的id
        store_password = user.hash_password # 存储密码

        # 用封装好的函数生成token
        token = util.crt_token(get_username, user.hash_password)

        if util.ckpwd(store_password,hash_password): # 判断这俩家伙是否相等
            data={
                "code":200,     # 状态码，表示成功
                "msg" :"登录成功",  # 提示信息，表示操作成功的提示信息
                "token":token,   # token，用于验证用户身份
                "username":user.username,  # 用户名
                "id":user.id,  # 用户id，主键
                "email": user.email,  # 邮箱
                "phone_number": user.phone_number,  # 手机号码
                "real_name": user.real_name,  # 真实姓名
                "register_time": user.register_time.strftime('%Y-%m-%d %H:%M:%S'),  # 注册时间
                "last_time": user.last_time.strftime('%Y-%m-%d %H:%M:%S')  # 上次登录时间
            }
            return jsonify(data)  # 成功    链接数据库
        else:   # 密码哈希值不正确
            # print(store_password)                                                                                                                                                                                          print(get_hash_password)
            return jsonify({"code":402,"msg":"密码错误"})

# 注册 test 成功
@user.route('/user/register', methods=['POST'])
def register():
    info = request.get_json()  # 获取表单数据
    get_username = info.get('username')
    # print(get_username)#test
    get_password = info.get('password')  # 注意拿到的是password不是hash_password!不要写错了
    get_checkPassword = info.get('checkPassword')
    email = info.get('email')# 邮箱
    phone_number = info.get('phone_number')# 手机号
    real_name = info.get('real_name')# 姓名
    # 获取当前时间戳并将其保存在数据库的 register_time 中
    register_time = datetime.fromtimestamp(time.time())
    # 标黄但问题不大

    # 对于不符合要求的检验
    with app.app_context():  # 任何与数据库有关的操作都要在数据库app的下面
        user = User.query.filter_by(username=get_username).first()  # 在数据库中查找username，以及对应id
        # print(user)#test
        if (user != None):  # 查询是否存在用户信息（username）
            return jsonify(util.fail(403,"用户名已存在,请重新注册！"))
        #         # 用户信息可以注册
        #         # 问题4：密码长度和密码是否相同前端已经确认了，这里需要再次确认吗？
        if (get_password != get_checkPassword):
            return jsonify(util.fail(405,"两次密码输入不同,请重新注册！"))
        if (User.query.filter_by(phone_number=phone_number).first()):
            return jsonify(util.fail(406, "手机号已被注册,请重新注册！"))
        if (User.query.filter_by(email=email).first()):
            return jsonify(util.fail(407, "邮箱已被注册,请重新注册！"))

        # 用户名合理，数据库处理
        hash_password = util.hash(get_password)
        # print(fs.hash(str(123456)))   # 123456的哈希
        # 密码合理

        # 创建 User 对象并将其保存到数据库中
        user = User(username=get_username, hash_password=hash_password, email=email, phone_number=phone_number,
                    real_name=real_name, register_time=register_time, last_time=register_time)
        db.session.add(user)
        db.session.commit()

        # 整理用户信息，这里用户信息从数据库存取，响应正确则表示数据也正确读入数据库
        user = User.query.filter_by(username=get_username).first()  # 在数据库中查找username，以及对应id
        data = {
            "code": 200,  # 状态码，表示成功
            "msg": "注册成功",  # 提示信息，表示操作成功的提示信息
            "username": user.username,  # 用户名
            "id": user.id,  # 用户id，主键
            "email": user.email,  # 邮箱
            "phone_number": user.phone_number,  # 手机号码
            "real_name": user.real_name,  # 真实姓名
            "register_time": user.register_time.strftime('%Y-%m-%d %H:%M:%S'),  # 注册时间
            "last_time": user.last_time.strftime('%Y-%m-%d %H:%M:%S')  # 上次登录时间
        }
        return jsonify(data)

from flask import Flask
from models import db
from views import bp as profile_bp


def create_app():
    app = Flask(__name__)

    # 配置数据库连接属性示例，具体根据实际情况修改以下内容
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host:port/db_name'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化Flask扩展模块db
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(profile_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)
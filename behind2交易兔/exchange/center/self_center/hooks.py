from flask import request, session, url_for,redirect
from .views import cms_bp


# 钩子函数 ,所有操作前执行该方法，判断当前界面是否是登录界面,不是就将url重定向到登录界面
@cms_bp.before_request
def before_request():
    print(request.path)                                         # 输出的是网页url的后缀，即/cms/login/
    if not request.path.endswith(url_for('cms.login')):    # 判断当前所在url是否是/cms/login/，不是代表不在后台登录界面
        user_id = session.get('user_id')                        # 登陆之后，获取登录时候记录的session中的user_id
        if not user_id:                                         # 若没有user_id，说明登录不成功
            return redirect(url_for('cms.login'))          # 重定向到后台登录界面


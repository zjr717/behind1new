'''functions'''
import hashlib,random,string

import datetime
import jwt
import hashlib

# ==============================================================#
# 加密key，应该存放在环境变量或者配置文件中，不能明文写在程序中
with open('SECRET_KEY.txt', encoding='utf-8') as file_obj:  # 将秘钥写在配置文件中
    contents = file_obj.read()
SECRET_KEY = contents.rstrip()  # 秘钥
# ==============================================================#

# 用来将密码用哈希算法加密的算法
def hash(password:str):
    # 使用SHA-256算法对密码进行哈希，并将结果转换为十六进制字符串。
    hash_obj = hashlib.sha256(password.encode('utf-8'))
    hash_password = hash_obj.hexdigest()
    return hash_password

# 失败
def fail(code,msg):
    return {"code":code, "msg":msg}

# 密码校验.看看get值与数据库中的值（哈希值）是否相等
def ckpwd(get_password,store_password):
    return get_password==store_password

# 可以使用如下代码来生成token
def crt_token(username,password):
    # 定义jwt的过期时间。前一个是获取当前时间
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    # 定义jwt的payload，这里可以存储一些必要的用户信息或者其他验证信息
    # 例如用户ID、用户名、权限、角色等等
    payload = {
        'id': '1',  # 在数据库查
        'username': username,
        'password': password,
        'iat': datetime.datetime.utcnow(),
        # 'iat'是一个JWT (ISONWeb Tokens)中的标准声明，表示"issued at"，即生成token的时间。
        # 这个时间戳可以用来验证token的有效期，以及防止token被重放攻击。
        # iat,是使用`daterime dateiome.utcnow()函救生成的，表示当前的UTC时间。这个时间戳会被加入到JWT的负载信息中，作为token的一个声明，用于验证token是否合法。
        'exp': expire
    }
    # 调用jwt encode方法生成token.测试成功
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')  # token生成，返回前端
    return token
    # 其中，payload是一个字典，用于存储一些必要的用户信息或者其他验证信息。iat字段表示jwt的签发时间，exp字段表示jwt的过期时间。算法使用HS256可以保证加密安全性。
    # 最后得到的token可以发送给客户端，并在后续的请求中作为身份验证凭据传递。在服务端接收到请求时，可以使用jwt.decode方法对token进行解码和验证，判断token是否合法和过期。
    # payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

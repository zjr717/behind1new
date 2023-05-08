DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'cyy'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}'.format(
    DIALECT,
    DRIVER,
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
    DATABASE
)

# 便于调试
TEMPLATES_AUTO_RELOAD = True
SEND_FILE_MAX_AGE_DEFAULT = 0
SQLALCHEMY_TRACK_MODIFICATIONS = True

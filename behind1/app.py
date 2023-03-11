from flask import Flask
from flask_cors import CORS
from behind1.database import init_db
from behind1.user.views import user_bp
from behind1.search.views import search_bp
from behind1.history.views import history_bp
from behind1.configs import Config, DevelopmentConfig

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(DevelopmentConfig)
app.secret_key = Config.SECRET_KEY


app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(history_bp, url_prefix='/history')

if __name__ == '__main__':
    init_db(app)
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
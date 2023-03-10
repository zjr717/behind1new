from flask import Flask
from flask_cors import CORS
from database import db
from user.views import user_bp
from configs import config
from search.views import search_bp
from history.views import history_bp

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = config.SECRET_KEY
db.init_app(app)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(search_bp,url_prefix='/search')
app.register_blueprint(history_bp,url_prefix='/user')
CORS(app, supports_credentials=True)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
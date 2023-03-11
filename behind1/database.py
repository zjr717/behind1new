from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"autocommit": False, "autoflush": False})


def init_db(app):
    with app.app_context():
        db.create_all()
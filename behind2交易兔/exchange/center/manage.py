from flask import Manager
from flask import Migrate, MigrateCommand
from exts import db
from behind2交易兔.exchange.center.self_info.app import app

manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()

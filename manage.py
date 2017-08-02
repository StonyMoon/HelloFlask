#coding:utf8
from flask_migrate import MigrateCommand , Migrate
from app import create_app,db
from flask_script import Manager
app = create_app()
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
if __name__ == '__main__':
    app.run()
    # manager.run()


#coding:utf8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from flask_login import LoginManager
from config import Config
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_migrate import Migrate,MigrateCommand
mail = Mail()
bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'#好像是受到保护的页面会转跳到这个页面里
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    return app
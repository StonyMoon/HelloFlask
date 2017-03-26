class Config():
    SECRET_KEY = 'ZXNMCBZXMNCBMNZXB'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIN_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '934998206@qq.com'
    MAIL_PASSWORD = 'dvskzmbhhzlnbfcd'
    FLASKY_ADMIN = '934998206@qq.com'
    PAGE = 20
    @staticmethod
    def init_app(app):
        pass

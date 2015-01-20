class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'dae', 'xml'])
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE = '/tmp/flaskr.db'
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'


class TestingConfig(Config):
    TESTING = True

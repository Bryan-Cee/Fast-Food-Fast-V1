import os


class Default:
    """Base configuration."""
    DEBUG = False
    DBNAME = os.getenv('DBNAME')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')


class DevelopmentConfig(Default):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Default):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    DBNAME = os.getenv('TESTDBNAME')


class ProductionConfig(Default):
    """Production configuration."""
    DEBUG = False
    DBNAME = os.getenv('DBNAME')
    SECRET_KEY = 'secret_key'


app_configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

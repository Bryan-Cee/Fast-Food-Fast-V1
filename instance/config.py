import os


class Default:
    """Base configuration."""
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')


class DevelopmentConfig(Default):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Default):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv('DATABASE_URL')


class ProductionConfig(Default):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')


app_configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

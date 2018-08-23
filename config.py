import os

class Config(object):
	"""
	Common configurations
	"""

	DEBUG = True
	SECRET_KEY = "itsasecret"

class DevelopmentConfig(Config):
	"""
	Development configurations
	"""

	DEBUG = True
	SECRET_KEY = "itsasecret"
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
	# SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class ProductionConfig(Config):
	"""
	Production configurations
	"""
	DEBUG = False
	TESTING = False
	SECRET_KEY = "itsasecret"
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
	JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class TestingConfig(Config):
	"""
	Testing configurations
	"""

	TESTING = True
	SECRET_KEY = "itsasecret"

app_config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	'testing': TestingConfig
}
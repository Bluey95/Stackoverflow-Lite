import os

class Config(object):
	"""
	Common configurations
	"""

	DEBUG = True
	SECRET_KEY = os.getenv("SECRET")

class DevelopmentConfig(Config):
	"""
	Development configurations
	"""

	DEBUG = True

class ProductionConfig(Config):
	"""
	Production configurations
	"""
	DEBUG = False
	TESTING = False

class TestingConfig(Config):
	"""
	Testing configurations
	"""

	TESTING = True

app_config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	'testing': TestingConfig
}
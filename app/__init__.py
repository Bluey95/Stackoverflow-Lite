import os
from config import app_config
# third-party imports
from flask import Flask

# local imports
from config import app_config

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # print(app_config.get('FLASK_CONFIG'))
    # print('*'*123)
    app.config.from_object(app_config[os.environ.get('FLASK_CONFIG')])

    from .questions import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .users import user_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1/auth')

    return app
import os
from config import app_config

# third-party imports
from flask import Flask, redirect,request, jsonify

# local imports
from config import app_config

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    # print(app_config.get('FLASK_CONFIG'))
    # print('*'*123)
    app.config.from_object(app_config[os.getenv('FLASK_CONFIG')])

    from .questions import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v2')

    from .users import user_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v2/auth')


    @app.route('/')
    def hello_world():
        return redirect("/api/v2/questions", code=302)

    API_PATH_PREFIX = '/api/'
    API_PATH_INDEX = '/'

    # @app.errorhandler(404)
    # def page_not_found_error(error):
    #     if request.path.startswith(API_PATH_PREFIX):
    #         return jsonify({'error': True, 'msg': 'API endpoint {!r} does not exist on this server'.format(request.path)}), error.code

    # @app.errorhandler(405)
    # def method_not_allowed_error(error):
    #     if request.path.startswith(API_PATH_INDEX):
    #         return jsonify({'error': True, 'msg': 'Please use the valid api urls'.format(request.path)}), error.code

    # @app.errorhandler(500)
    # def method_not_allowed_error(error):
    #     if request.path.startswith(API_PATH_INDEX):
    #         return jsonify({'error': True, 'msg': 'Oops! Something went wrong'.format(request.path)}), error.code
    return app
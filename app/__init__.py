import os
from config import app_config
from flask_cors import CORS

# third-party imports
from flask import Flask, redirect,request, jsonify, render_template

# local imports
from config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.url_map.strict_slashes = False
    # print(app_config.get('FLASK_CONFIG'))
    # print('*'*123)
    app.config.from_object(app_config[os.getenv('FLASK_CONFIG')])

    from .questions import api as api_blueprint
    CORS(app.register_blueprint(api_blueprint, url_prefix='/api/v2'))

    from .users import user_api as api_blueprint
    CORS(app.register_blueprint(api_blueprint, url_prefix='/api/v2/auth'))


    @app.route("/")
    def questions():  
        return render_template('index.html')

    @app.route("/index.html")
    def questions_index():  
        return render_template('index.html')

    @app.route("/profile.html")
    def profile():  
        return render_template('profile.html')
    
    @app.route("/signin.html")
    def signin():  
        return render_template('signin.html')
    
    @app.route("/signup.html")
    def signup():  
        return render_template('signup.html')

    @app.route("/userask.html")
    def userask():  
        return render_template('userask.html')

    @app.route("/userquestions.html")
    def userquestions():  
        return render_template('userquestions.html')

    @app.route("/viewquestions.html")
    def viewquestions():  
        return render_template('viewquestions.html')

    if __name__ == "__main__":  
        app.run(debug=True)

    API_PATH_PREFIX = '/api/'
    API_PATH_INDEX = '/'

    @app.errorhandler(404)
    def page_not_found_error(error):
        if request.path.startswith(API_PATH_PREFIX):
            return jsonify({'error': True, 'msg': 'API endpoint {!r} does not exist on this server'.format(request.path)}), error.code

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        if request.path.startswith(API_PATH_INDEX):
            return jsonify({'error': True, 'msg': 'Please use the valid api urls'.format(request.path)}), error.code

    # @app.errorhandler(500)
    # def method_not_allowed_error(error):
    #     if request.path.startswith(API_PATH_INDEX):
    #         return jsonify({'error': True, 'msg': 'Oops! Something went wrong'.format(request.path)}), error.code
    
    return app
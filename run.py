import os

from app import create_app
from flask_cors import CORS, cross_origin

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run()

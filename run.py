import os

from app import create_app
from flask_restful import Api

@pytest.fixture
config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
api = Api(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run()

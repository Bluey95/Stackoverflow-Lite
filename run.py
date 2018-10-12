import os

from app import create_app
from migrate import main


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
main()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run()

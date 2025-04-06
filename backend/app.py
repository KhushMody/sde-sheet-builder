from flask import Flask
from flask_cors import CORS
from .routes import register_routes
from .models import db
from .config import Config

def create_app(config_class=Config, test_config=None):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
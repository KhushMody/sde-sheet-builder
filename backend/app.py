from flask import Flask
from flask_cors import CORS
from .routes import register_routes
from .models import db
from .config import Config

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    # Initialize CORS with app
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
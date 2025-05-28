from flask import Flask, session # Added session for key_func
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from flask_limiter import Limiter # Import Limiter
from flask_limiter.util import get_remote_address # Import get_remote_address
from .routes import register_routes # General routes
from .models import db
from .config import Config
from .routes.auth import auth_bp # Import the auth blueprint

# Initialize OAuth object at the module level
oauth = OAuth()

# Define the key function for rate limiting
def get_user_identifier():
    # Check if user is in session and has an email (consistent with Google OAuth userinfo)
    if 'user' in session and isinstance(session['user'], dict) and session['user'].get('email'):
        return session['user']['email']
    return get_remote_address

# Initialize Limiter at the module level
limiter = Limiter(
    key_func=get_user_identifier,
    default_limits=["200 per day", "50 per hour"], # Default global limits
    storage_uri="memory://" # Use memory storage for simplicity; consider Redis for production
)

def create_app(config_class=Config, test_config=None):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if test_config:
        app.config.update(test_config)

    # Set secret key for session management (used by Authlib)
    app.secret_key = app.config['SECRET_KEY']
    
    # Ensure SERVER_NAME is explicitly available if needed by Flask for URL generation,
    # though Authlib primarily uses it from app.config for redirect URIs.
    # app.config.from_object(Config) should have already loaded it.
    app.config['SERVER_NAME'] = app.config.get('SERVER_NAME')

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize Limiter with the app instance
    limiter.init_app(app)

    # Initialize the global oauth object with the app instance
    oauth.init_app(app) 
    
    # Register the Google client with the global oauth object.
    # It's important that this happens after oauth.init_app(app)
    # and that it uses the globally defined 'oauth' object.
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Register blueprints
    app.register_blueprint(auth_bp) # Register the auth blueprint
    # The original register_routes(app) can be called before or after,
    # depending on desired route precedence or organization.
    # If register_routes also defines blueprints, order might matter.
    # For now, assuming it registers other distinct routes.
    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
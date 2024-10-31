from flask import Flask
from flask_cors import CORS
from app.config import get_config
from app.api import api, init_app
from .logger import log

def create_app():
    app = Flask(__name__)

    # Get the config class based on the environment
    config_class = get_config()
    app.config.from_object(config_class)

    # Logging the environment and enabling CORS
    log(f'*{config_class.ENV.capitalize()}* environment detected, enabling CORS for specific domains.')
    
    # Enable CORS for specific origins based on the environment
    # log(f'Allowed origins: {config_class.CORS_ORIGINS}')
    log(f'Allowed origins: {config_class.CORS_ORIGINS}', level='WARNING')

    CORS(app, 
         resources={r"/api/*": {"origins": config_class.CORS_ORIGINS}},
         supports_credentials=True,
         methods=["GET", "POST", "OPTIONS", "DELETE", "PUT"],  # Add other methods as needed
         allow_headers=["Content-Type", "Authorization"],      # Add other necessary headers
    )

    # Initialize the app
    init_app(app)
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    return app


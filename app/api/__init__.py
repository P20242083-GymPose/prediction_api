from flask import Blueprint
from .blueprint import blueprint
from .utils import log

# Create a Blueprint instance for the API
api = Blueprint('api', __name__)

# Register the blueprints
api.register_blueprint(blueprint)


# Initialize any required services or utilities here
def init_app(app):
    # Initialize the logger
    log(f"{app.config['ENV']} environment initialized", level='INFO')
    


__all__ = ['api', 'api_v2', 'init_app']


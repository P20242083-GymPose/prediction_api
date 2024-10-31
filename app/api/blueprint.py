from flask import Blueprint

blueprint = Blueprint('api', __name__)

# Import controllers to register routes with the blueprint
from app.api import controllers

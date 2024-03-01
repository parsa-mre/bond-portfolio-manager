from flask_smorest import Blueprint

blp = Blueprint('bond', __name__, url_prefix='/bond')

from .routes import *

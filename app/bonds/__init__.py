from flask_smorest import Blueprint

blp = Blueprint('bond', __name__, url_prefix='/bonds')

from .routes import *

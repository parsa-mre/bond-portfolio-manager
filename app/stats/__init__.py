from flask_smorest import Blueprint

blp = Blueprint('stats', __name__, url_prefix='/stats')

from .routes import *

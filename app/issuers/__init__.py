from flask_smorest import Blueprint

blp = Blueprint('issuer', __name__, url_prefix='/issuers')

from .routes import *

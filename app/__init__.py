from flask import Flask
from config import Config
from app.extensions import db
from flask_smorest import Api
from flask_cors import CORS


def create_app(config_class=Config):
    app = Flask(__name__)
    # CORS(app, resources={r"/*": {"origins": "*"}})
    CORS(app)
    app.config.from_object(config_class)
    # CORS(app, origins="")
    # Initialize Flask extensions here
    from app.models import Bond, Issuer

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints here
    api = Api(app)

    from app.bonds import blp as bonds_blp
    api.register_blueprint(bonds_blp, )

    from app.issuers import blp as issuers_blp
    api.register_blueprint(issuers_blp)

    from app.stats import blp as stats_blp
    api.register_blueprint(stats_blp)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    # CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    # CORS(app)
    return app

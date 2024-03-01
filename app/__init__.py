from flask import Flask
from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.bonds import blp as bonds_blp
    app.register_blueprint(bonds_blp)

    from app.issuers import blp as issuers_blp
    app.register_blueprint(issuers_blp)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

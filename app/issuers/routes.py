from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from app.schemas import IssuerSchemaPlain
from app.issuers import blp
from flask import request
from flask_smorest import abort
from app.extensions import db
from app.models import Issuer


@blp.route("/")
class IssuerGroupView(MethodView):
    @blp.arguments(IssuerSchemaPlain)
    @blp.response(201, IssuerSchemaPlain)
    def post(self, issuer_data):
        issuer = Issuer(**issuer_data)
        try:
            db.session.add(issuer)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e))

        return issuer

    @blp.response(200, IssuerSchemaPlain(many=True))
    def get(self):
        return Issuer.query.all()


@blp.route("/<int:issuer_id>")
class IssuerView(MethodView):
    @blp.response(200, IssuerSchemaPlain)
    def get(self, issuer_id):
        issuer = Issuer.query.get_or_404(issuer_id)
        return issuer

    def delete(self, issuer_id):
        issuer = Issuer.query.get_or_404(issuer_id)
        if issuer.bonds.first() is not None:
            abort(400, message="Issuer cannot be deleted. Issuers Bonds must be deleted first.")
        db.session.delete(issuer)
        db.session.commit()
        return {"message": "issuer deleted"}, 204

    @blp.arguments(IssuerSchemaPlain)
    @blp.response(200, IssuerSchemaPlain)
    def put(self, issuer_data, issuer_id):
        print("inside put")
        issuer = Issuer.query.get_or_404(issuer_id)
        for key, value in issuer_data.items():
            setattr(issuer, key, value)
        db.session.commit()
        return issuer

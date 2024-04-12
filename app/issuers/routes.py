from flask.views import MethodView
from flask_cors import cross_origin
from sqlalchemy.exc import SQLAlchemyError

from app.schemas import IssuerSchemaPlain, IssuerSchemaPaginated
from app.issuers import blp
from flask import request
from flask_smorest import abort
from app.extensions import db
from app.models import Issuer

HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
    "Access-Control-Allow-Headers": "Access-Control-Request-Headers,Access-Control-Allow-Methods,Access-Control-Allow-Headers,Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept"
}


@blp.route("")
class IssuerGroupView(MethodView):
    @blp.arguments(IssuerSchemaPlain)
    @blp.response(201, IssuerSchemaPlain, headers=HEADERS)
    def post(self, issuer_data):
        issuer = Issuer(**issuer_data)
        try:
            db.session.add(issuer)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e))

        return issuer

    @blp.response(200, IssuerSchemaPaginated, headers=HEADERS)
    @blp.paginate()
    def get(self, pagination_parameters):
        total = Issuer.query.count()
        next = pagination_parameters.page if pagination_parameters.page + 1 > total else pagination_parameters.page + 1
        prev = pagination_parameters.page if pagination_parameters.page - 1 < 1 else pagination_parameters.page - 1
        response = {
            "data": Issuer.query.paginate(page=pagination_parameters.page, per_page=pagination_parameters.page_size),
            "meta": {
                "total": Issuer.query.count(),
                "page": pagination_parameters.page,
                "per_page": pagination_parameters.page_size,
                "links": {
                    "self": request.url,
                    "next": request.url + f"?page={next}&page_size={pagination_parameters.page_size}",
                    "prev": request.url + f"?page={prev}&page_size={pagination_parameters.page_size}"
                }
            }
        }
        return response


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
        issuer = Issuer.query.get_or_404(issuer_id)
        for key, value in issuer_data.items():
            setattr(issuer, key, value)
        db.session.commit()
        return issuer

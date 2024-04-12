from sqlalchemy.exc import SQLAlchemyError

from app.bonds import blp
from flask import Flask, request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
import uuid
from app.models import Bond, BondPrice
from app.extensions import db
from app.schemas.bond_schemas import BondSchemaPlain, BondPriceSchemaPlain, BondSchemaPaginated

HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
    "Access-Control-Allow-Headers": "Access-Control-Request-Headers,Access-Control-Allow-Methods,Access-Control-Allow-Headers,Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept"
}

@blp.route("")
class BondGroupView(MethodView):
    @blp.arguments(BondSchemaPlain)
    @blp.response(201, BondSchemaPlain, headers=HEADERS)
    def post(self, bond_data):
        bond = Bond(**bond_data)
        try:
            db.session.add(bond)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e))
        return bond

    @blp.response(200, BondSchemaPaginated, headers=HEADERS)
    @blp.paginate()
    def get(self, pagination_parameters):
        print("here")
        total = Bond.query.count();
        next = pagination_parameters.page if pagination_parameters.page + 1 > total else pagination_parameters.page + 1
        prev = pagination_parameters.page if pagination_parameters.page - 1 < 1 else pagination_parameters.page - 1
        response = {
            "data": Bond.query.paginate(page=pagination_parameters.page, per_page=pagination_parameters.page_size),
            "meta": {
                "total": Bond.query.count(),
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


@blp.route("/<int:bond_id>")
class BondView(MethodView):
    @blp.response(200, BondSchemaPlain)
    def get(self, bond_id):
        bond = Bond.query.get_or_404(bond_id)
        return bond

    def delete(self, bond_id):
        bond = Bond.query.get_or_404(bond_id)
        db.session.delete(bond)
        db.session.commit()
        return {"message": "bond deleted"}, 204

    @blp.arguments(BondSchemaPlain)
    @blp.response(200, BondSchemaPlain)
    def put(self, bond_data, bond_id):
        bond = Bond.query.get_or_404(bond_id)
        for key, value in bond_data.items():
            setattr(bond, key, value)
        db.session.commit()
        return bond


# bond prices
@blp.route("/<int:bond_id>/prices")
class BondPriceGroupView(MethodView):
    @blp.arguments(BondPriceSchemaPlain)
    @blp.response(201, BondPriceSchemaPlain)
    def post(self, bond_price_data, bond_id):
        bond_price = BondPrice(**bond_price_data)
        bond_price.bond_id = bond_id
        try:
            db.session.add(bond_price)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e))
        return bond_price

    @blp.response(200, BondPriceSchemaPlain(many=True))
    def get(self, bond_id):
        bond = Bond.query.get_or_404(bond_id)
        return bond.prices.all()
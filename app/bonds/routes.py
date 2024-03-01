from sqlalchemy.exc import SQLAlchemyError

from app.bonds import blp
from flask import Flask, request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
import uuid
from app.models import Bond
from app.extensions import db
from app.schemas.bond_schemas import BondSchemaPlain


@blp.route("/")
class BondGroupView(MethodView):
    @blp.arguments(BondSchemaPlain)
    @blp.response(201, BondSchemaPlain)
    def post(self, bond_data):
        bond = Bond(**bond_data)
        try:
            db.session.add(bond)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e))
        return bond

    @blp.response(200, BondSchemaPlain(many=True))
    def get(self):
        return Bond.query.all()


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

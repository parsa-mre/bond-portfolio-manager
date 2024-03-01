import marshmallow as ma
from .issuer_schemas import IssuerSchemaPlain


class BondSchemaPlain(ma.Schema):
    id = ma.fields.Str(dump_only=True)

    issuer_id = ma.fields.Integer(required=True, load_only=True)
    issuer = ma.fields.Nested(IssuerSchemaPlain(), only=["id", "name"], dump_only=True)
    issuance_date = ma.fields.Date(required=True)

    sale_date = ma.fields.Date(required=False)
    sale_price = ma.fields.Float(required=False)

    maturation = ma.fields.Date(required=True)
    face_value = ma.fields.Float(required=True)
    coupon = ma.fields.Float(required=True)

    @ma.validates_schema
    def validate_dates(self, data, **kwargs):
        sale_date = data.get("sale_date")
        sale_price = data.get("sale_price")
        issuance_date = data.get("issuance_date")

        if sale_date and sale_price:
            if sale_date < issuance_date:
                raise ma.ValidationError("Sale date cannot be before issuance date")

            if data["maturation"] < issuance_date:
                raise ma.ValidationError("Maturation date cannot be before issuance date")

            if sale_date and sale_date > data.get("maturation"):
                raise ma.ValidationError("Sale date cannot be after maturation date")

        if ((sale_price is None and sale_date is not None) or
                (sale_price is not None and sale_date is None)):
            raise ma.ValidationError("Both sale date and sale price must be either provided or not provided.")




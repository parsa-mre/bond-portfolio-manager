import marshmallow as ma


class IssuerSchemaPlain(ma.Schema):
    id = ma.fields.Str(dump_only=True)
    name = ma.fields.Str(required=True)
    country = ma.fields.Str(required=True)
    credit_rating = ma.fields.Str(required=True)
    industry = ma.fields.Str(required=True)

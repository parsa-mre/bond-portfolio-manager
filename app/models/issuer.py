from app.extensions import db


class Issuer(db.Model):
    __tablename__ = "issuer_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    credit_rating = db.Column(db.String(80), nullable=False)
    industry = db.Column(db.String(80), nullable=False)
    county = db.Column(db.String(80), nullable=False)
    bonds = db.relationship("Bond", back_populates="bond_table", lazy="dynamic")

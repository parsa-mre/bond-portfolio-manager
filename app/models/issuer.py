from app.extensions import db


class Issuer(db.Model):
    __tablename__ = "issuer_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    credit_rating = db.Column(db.String(80), nullable=False)
    industry = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    bonds = db.relationship("Bond", back_populates="issuer", lazy="dynamic")

    def __repr__(self):
        return f"<Issuer {self.name}>"

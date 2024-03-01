from app.extensions import db


class Bond(db.Model):
    __tablename__ = "bond_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    issuer_id = db.Column(db.Integer, db.ForeignKey("issuer_table.id"), nullable=False)
    issuer = db.relationship("Issuer", back_populates="bonds")
    issuance_date = db.Column(db.Date, nullable=False)

    sale_date = db.Column(db.Date, nullable=True)
    sale_price = db.Column(db.Float, nullable=True)

    maturation = db.Column(db.Date, nullable=False)
    face_value = db.Column(db.Float, nullable=False)
    coupon = db.Column(db.Float, nullable=False)

    prices = db.relationship("BondPrice", back_populates="bond", lazy="dynamic")

    def __repr__(self):
        return f"<Bond id:{self.id}, v:{self.face_value}, c:{self.coupon}, m:{self.maturation}>"


class BondPrice(db.Model):
    __tablename__ = "bond_price_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bond_id = db.Column(db.Integer, db.ForeignKey("bond_table.id"), nullable=False)
    bond = db.relationship("Bond", back_populates="prices")
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<BondPrice {self.bond_id}>"

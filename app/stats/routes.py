from flask import jsonify
from flask.views import MethodView
from app.models import Bond, BondPrice, Issuer
from app.extensions import db
from app.stats import blp

@blp.route("/countries")
class CountryStats(MethodView):

    def get(self):
        bonds = db.session.query(Bond, BondPrice.price, Bond.issuer_id). \
            join(Bond.prices).all()

        country_price_sums = {}
        for bond, price, issuer_id in bonds:
            country_price_sums.setdefault(bond.issuer_id, 0)
            country_price_sums[bond.issuer_id] += price

        country_stats = {}
        for issuer_id, total_price in country_price_sums.items():
            issuer_name = db.session.query(Issuer.country).filter_by(id=issuer_id).scalar()
            country_stats[issuer_name] = total_price

        return jsonify(country_stats)

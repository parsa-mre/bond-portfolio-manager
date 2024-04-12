from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models.bond import Bond, BondPrice
from app.models.issuer import Issuer
from faker import Faker
import random
from datetime import datetime, timedelta
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)
fake = Faker()

industries = [
    "Accounting",
    "Airlines/Aviation",
    "Alternative Dispute Resolution",
    "Alternative Medicine",
    "Animation",
    "Apparel & Fashion",
    "Architecture & Planning",
    "Arts & Crafts",
    "Automotive",
    "Aviation & Aerospace",
    "Banking",
    "Biotechnology",
    "Broadcast Media",
    "Building Materials",
    "Business Supplies & Equipment",
    "Capital Markets",
    "Chemicals",
    "Civic & Social Organization",
    "Civil Engineering",
    "Commercial Real Estate",
    "Computer & Network Security",
    "Computer Games",
    "Computer Hardware",
    "Computer Networking",
    "Computer Software",
    "Construction",
    "Consumer Electronics",
    "Consumer Goods",
    "Consumer Services",
    "Cosmetics",
    "Dairy",
    "Defense & Space",
    "Design",
    "Education Management",
    "E-learning",
    "Electrical & Electronic Manufacturing",
    "Entertainment",
    "Environmental Services",
    "Events Services",
    "Executive Office",
    "Facilities Services",
    "Farming",
    "Financial Services",
    "Fine Art",
    "Fishery",
    "Food & Beverages",
    "Food Production",
    "Fundraising",
    "Furniture",
    "Gambling & Casinos",
    "Glass, Ceramics & Concrete",
    "Government Administration",
    "Government Relations",
    "Graphic Design",
    "Health, Wellness & Fitness",
    "Higher Education",
    "Hospital & Health Care",
    "Hospitality",
    "Human Resources",
    "Import & Export",
    "Individual & Family Services",
    "Industrial Automation",
    "Information Services",
    "Information Technology & Services",
    "Insurance",
    "International Affairs",
    "International Trade & Development",
    "Internet",
    "Investment Banking/Venture",
    "Investment Management",
    "Judiciary",
    "Law Enforcement",
    "Law Practice",
    "Legal Services",
    "Legislative Office",
    "Leisure & Travel",
    "Libraries",
    "Logistics & Supply Chain",
    "Luxury Goods & Jewelry",
    "Machinery",
    "Management Consulting",
    "Maritime",
    "Marketing & Advertising",
    "Market Research",
    "Mechanical or Industrial Engineering",
    "Media Production",
    "Medical Device",
    "Medical Practice",
    "Mental Health Care",
    "Military",
    "Mining & Metals",
    "Motion Pictures & Film",
    "Museums & Institutions",
    "Music",
    "Nanotechnology",
    "Newspapers",
    "Nonprofit Organization Management",
    "Oil & Energy",
    "Online Publishing",
    "Outsourcing/Offshoring",
    "Package/Freight Delivery",
    "Packaging & Containers",
    "Paper & Forest Products",
    "Performing Arts",
    "Pharmaceuticals",
    "Philanthropy",
    "Photography",
    "Plastics",
    "Political Organization",
    "Primary/Secondary",
    "Printing",
    "Professional Training",
    "Program Development",
    "Public Policy",
    "Public Relations",
    "Public Safety",
    "Publishing",
    "Railroad Manufacture",
    "Ranching",
    "Real Estate",
    "Recreational",
    "Facilities & Services",
    "Religious Institutions",
    "Renewables & Environment",
    "Research",
    "Restaurants",
    "Retail",
    "Security & Investigations",
    "Semiconductors",
    "Shipbuilding",
    "Sporting Goods",
    "Sports",
    "Staffing & Recruiting",
    "Supermarkets",
    "Telecommunications",
    "Textiles",
    "Think Tanks",
    "Tobacco",
    "Translation & Localization",
    "Transportation/Trucking/Railroad",
    "Utilities",
    "Venture Capital",
    "Veterinary",
    "Warehousing",
    "Wholesale",
    "Wine & Spirits",
    "Wireless",
    "Writing & Editing"
]


def weighted_country_selection():
    more_stable_countries = ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Italy', 'Spain',
                             'Netherlands', 'Switzerland', 'Sweden', 'Norway', 'Denmark', 'Belgium', 'Austria',
                             'Finland', 'Ireland', 'Portugal', 'Greece', 'Luxembourg', 'Iceland', 'Australia',
                             'New Zealand', 'Japan']
    other_countries = ['Brazil', 'Malaysia', 'Ukraine', 'Nigeria', 'Chile', 'Paraguay', 'Peru', 'Mexico', 'Turkey',
                       'Colombia', 'Argentina', 'Morocco', 'Philippines', 'Swaziland', 'Egypt', 'Ecuador', 'Haiti',
                       'Kenya', 'Azerbaijan', 'Turkmenistan', 'Iceland', 'Korea', 'India']

    # Adjust the weights for western and other countries
    countries = more_stable_countries + other_countries
    weights = [6] * len(more_stable_countries) + [1] * len(other_countries)

    return random.choices(countries, weights=weights)[0]


def generate_fake_data(num_records):
    fake_data = []
    for _ in range(num_records):
        name = fake.company()
        credit_rating = random.choice(
            ['BBB', 'AAA', 'AA', 'A', 'BBB', 'AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'CC', 'C', 'D'])
        industry = random.choice(industries)
        country = weighted_country_selection()
        fake_data.append({
            'name': name,
            'credit_rating': credit_rating,
            'industry': industry,
            'country': country
        })
    return fake_data


def generate_fake_issuers():
    fake_issuers = generate_fake_data(20)
    for issuer in fake_issuers:
        issuer = Issuer(**issuer)
        db.session.add(issuer)
    db.session.commit()


def generate_mock_data(num_bonds=60, num_prices_per_bond=5):
    for _ in range(num_bonds):
        issuer_id = random.randint(1, 20)  # Assuming 10 different issuers
        issuance_date = fake.date_between(start_date='-10y', end_date='today')
        maturation = issuance_date + timedelta(days=random.randint(365, 10*365))
        face_value = random.randint(1000, 10000)
        coupon = random.uniform(0.01, 0.1)

        bond = Bond(
            issuer_id=issuer_id,
            issuance_date=issuance_date,
            maturation=maturation,
            face_value=face_value,
            coupon=coupon
        )
        db.session.add(bond)

        for _ in range(num_prices_per_bond):
            price = random.uniform(0.5, 1.5) * face_value
            date = issuance_date + timedelta(days=random.randint(1, (maturation - issuance_date).days))

            bond_price = BondPrice(
                bond=bond,
                price=price,
                date=date
            )
            db.session.add(bond_price)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # generate_fake_issuers()
        generate_mock_data()
        print('Fake data generated successfully!')

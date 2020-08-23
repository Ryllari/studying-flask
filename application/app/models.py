from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def config_db(app):
    db.init_app(app)
    app.db = db


class DIDNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(17))
    monthyPrice = db.Column(db.Numeric(precision=8, scale=2, decimal_return_scale=2))
    setupPrice = db.Column(db.Numeric(precision=8, scale=2, decimal_return_scale=2))
    currency = db.Column(db.String(5))

    def __repr__(self):
        return f'<[{self.id}] DID Number - {self.value}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def as_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "monthyPrice": str(self.monthyPrice),
            "setupPrice": str(self.setupPrice),
            "currency": self.currency
        }

from db import db


class ClientModel(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False,  nullable=True)
    last_name = db.Column(db.String(80), unique=False,  nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)

    book_rent = db.relationship("BookRentModel", back_populates="client", lazy="dynamic")
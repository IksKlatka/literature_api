from db import db

class BookModel(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150), unique=True, nullable = False)
    author = db.Column(db.String(80), unique= False, nullable= False)
    genre = db.Column(db.String(80), unique=False)
    year_published = db.Column(db.Integer, unique= False)
    status = db.Column(db.String, unique=False, nullable=False)
    times_rented = db.Column(db.Integer, unique=False, nullable=False)

    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), unique=False, nullable=False)

    country = db.relationship("CountryModel", back_populates="books")
    book_rents = db.relationship("BookRentModel", back_populates="books", lazy="joined")

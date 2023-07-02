from db import db

class BookModel(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150), unique=True, nullable = False)
    author = db.Column(db.String(80), unique= False, nullable= False)
    year_published = db.Column(db.Integer, uniwue= False)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), unique=False, nullable=False)
    country = db.relationship("CountryModel", back_populates="books")
from db import db

class CountryModel(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String, unique=True, nullable=False)
    continent = db.Column(db.String, unique=False, nullable= False)
    books = db.relationship("BookModel", back_populates="country",
                            lazy="dynamic", cascade="all, delete")
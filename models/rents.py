from db import db

class BookRentModel(db.Model):
    __tablename__ = "book_rent"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), unique=False, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), unique=False, nullable=False)
    date_rented = db.Column(db.Date, unique=False, nullable=False)
    date_returned = db.Column(db.Date, unique=False, nullable=True)
    status = db.Column(db.String, unique=False, nullable=False)

    books = db.relationship("BookModel", back_populates="book_rents")
    client = db.relationship("ClientModel", back_populates="book_rent")

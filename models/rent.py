import enum

from db import db

class RentStatus(enum.Enum): #note: for validation
    rented = "rented"
    extended = "rent extended"
    returned = "returned"

class BookRentModel(db.Model):
    __tablename__ = "book_rent"

    id = db.Column(db.Int(), primary_key=True)
    book_id = db.Column(db.Int(), db.ForeignKey("books.id"), unique=False, nullable=False)
    client_id = db.Column(db.Int(), db.ForeignKey("clients.id"), unique=False, nullable=False)
    date_rented = db.Column(db.Date(), unique=False, nullable=False)
    date_returned = db.Column(db.Date(), unique=False, nullable=True)
    status = db.Column(enum.Enum(['rented', 'extended', 'returned']), nullable=False, unique=False)

    book = db.relationship("BookModel", back_populates="book_rent", foreign_keys=[book_id])
    client = db.relationship("ClientModel", back_populates="book_rent", unique=False, nullable=False)
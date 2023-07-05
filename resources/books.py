from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from models import BookModel
from schema import BookSchema, UpdateBookSchema, PlainBookSchema
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("Books", __name__, description="Books CRUD.")

@blp.route('/book/<string:book_id>')
class Book(MethodView):
    @blp.response(200, BookSchema)
    def get(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        return book

    def delete(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()

        return {"message": "Book '{}' deleted.".format(book.title)}

    @blp.arguments(UpdateBookSchema)
    @blp.response(200, BookSchema)
    def put(self, book_data, book_id):

        book = BookModel.query.get(book_id)
        if book:
            book.title = book_data['title']
            book.author = book_data['author']
            book.genre = book_data['genre']
            book.year_published = book_data['year_published']
            book.country_id = book_data['country_id']
        else:
            book = BookModel(book_id, **book_data)

        db.session.add(book)
        db.session.commit()

        return book
@blp.route('/book')
class BookList(MethodView):
    @blp.response(201, BookSchema(many=True))
    def get(self):
        return BookModel.query.all()

    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def post(self, book_data):

        book = BookModel(**book_data)
        try:
            db.session.add(book)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "SQLAlchemyError occurred while inserting book.")

        return book


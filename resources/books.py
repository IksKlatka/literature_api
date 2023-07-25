from flask_smorest import Blueprint, abort
from flask.views import MethodView
import flask_jwt_extended as jwt
from flask import jsonify
from db import db
from models import BookModel, check_admins_permissions
from schema import BookSchema, UpdateBookSchema, PlainBookSchema
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("Books", __name__, description="Books CRUD.")

@blp.route('/book/<string:book_id>')
class Book(MethodView):
    @blp.response(200, BookSchema)
    def get(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        return book

    @jwt.jwt_required()
    def delete(self, book_id):

        if check_admins_permissions(jwt.get_jwt_identity()):
            book = BookModel.query.get_or_404(book_id)
            db.session.delete(book)
            db.session.commit()
            return jsonify({"message": f"Book {book.title} deleted successfully."}), 200
        return jsonify({"message": "Lack of permissions."}), 403


    @jwt.jwt_required()
    @blp.arguments(UpdateBookSchema)
    @blp.response(200, BookSchema)
    def put(self, book_data, book_id):

        if check_admins_permissions(jwt.get_jwt_identity()):
            book = BookModel.query.get(book_id)
            if book:
                book.title = book_data.get('title', book.title)
                book.author = book_data.get('author', book.author)
                book.genre = book_data.get('genre', book.genre)
                book.year_published = book_data.get('year_published', book.year_published)
                book.status = book_data.get('status', book.status)
                book.country_id = book_data.get('country_id', book.country_id)
            else:
                book = BookModel(id= book_id, **book_data)

            db.session.add(book)
            db.session.commit()

            return jsonify({"message": f"Book {book_data['title']} updated successfully."}), 201
        return jsonify({"message": "Lack of permissions."}), 403


@blp.route('/book')
class BookList(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        return BookModel.query.all()

    @jwt.jwt_required()
    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def post(self, book_data):

        if check_admins_permissions(jwt.get_jwt_identity()):
            book = BookModel(**book_data)
            try:
                db.session.add(book)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, "SQLAlchemyError occurred while inserting book.")

            return jsonify(
                {"message": f"Book {book_data['title']} by {book_data['author']} created successfully."}
            ), 201
        return jsonify({"message": "Lack of permissions."})




from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import flask_jwt_extended as jwt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from db import db
from models import BookRentModel, BookModel, check_admins_permissions, ClientModel
from schema import PlainRentSchema, UpdateRentSchema, UpdateBookSchema

blp = Blueprint("BookRental", __name__, description="Book rental CRUD.")


@blp.route('/rental/<string:rent_id>')
class BookRental(MethodView):

    @jwt.jwt_required()
    @blp.response(200, PlainRentSchema)
    def get(self, rent_id):
        if check_admins_permissions(jwt.get_jwt_identity()):
            book_rent = BookRentModel.query.filter_by(id=rent_id). \
                options(joinedload(BookRentModel.books),
                        joinedload(BookRentModel.client)).first()
            return book_rent

        return jsonify({"message": "Lack of permissions."})

    @jwt.jwt_required()
    def delete(self, rent_id):
        if check_admins_permissions(jwt.get_jwt_identity()):
            book_rent = BookRentModel.query.get_or_404(rent_id)
            db.session.delete(book_rent)
            db.session.commit()
            return jsonify({"message": f"Book {book_rent.id} deleted."})
        return jsonify({"message": "Lack of permissions."})


    @jwt.jwt_required()
    @blp.arguments(UpdateRentSchema)
    @blp.response(201, PlainRentSchema)
    def put(self, rent_data, rent_id):
        book_rent = BookRentModel.query.get(rent_id)
        book = BookModel.query.get(book_rent.book_id)
        client_id = jwt.get_jwt_identity()
        client = ClientModel.query.get_or_404(client_id)

        if book_rent:
            book_rent.date_returned = rent_data['date_returned']
            book_rent.status = rent_data['status']
            if rent_data['status'] == 'returned':
                book.status = 'available'
                client.no_books_rented += 1
        else:
            book_rent = BookRentModel(id=rent_id, **rent_data)

        db.session.add(book_rent)
        db.session.commit()

        return book_rent


@blp.route('/rental')
class ListBookRental(MethodView):

    @blp.response(200, PlainRentSchema(many=True))
    def get(self):
        return BookRentModel.query.all()

    @jwt.jwt_required()
    @blp.arguments(PlainRentSchema)
    @blp.response(201, PlainRentSchema)
    def post(self, rent_data):

        book = BookModel.query.get_or_404(rent_data['book_id'])
        book_rent = BookRentModel(**rent_data)

        if jwt.get_jwt_identity() != book_rent.client_id:
            return jsonify({"message": "You can rent books only for yourself."})
        if book.status != "available":
            return jsonify({"message": "This book is not available at this moment."})
        else:
            book.status = "rented"
            book.times_rented += 1
        try:
            db.session.add(book_rent)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "SQLAlchemyError occurred while inserting rent.")

        return jsonify({"message": "Rent created."}), 201



@blp.route("/rental/client/<int:client_id>")
class ListClientRents(MethodView):

    # todo: Client can only see all its book_rents!! sth's wrong here
    @jwt.jwt_required()
    @blp.response(200, PlainRentSchema(many=True))
    def get(self, client_id):

        client = ClientModel.query.get_or_404(client_id)
        if jwt.get_jwt_identity() == client_id or check_admins_permissions(client_id):
            rentals = BookRentModel.query.filter_by(client_id=client_id).all()
            if not rentals:
                return jsonify({"message": f"No rents for client with id {client_id}"})
            else:
                return rentals
        return jsonify({"message": "Lack of permissions."})


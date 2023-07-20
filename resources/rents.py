from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from db import db
from models import BookRentModel, BookModel, ClientModel
from schema import PlainRentSchema, UpdateRentSchema, UpdateBookSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("BookRental", __name__, description="Book rental CRUD.")


@blp.route('/rental/<string:rent_id>')
class BookRental(MethodView):

    # @jwt_required()
    @blp.response(200, PlainRentSchema)
    def get(self, rent_id):
        book_rent = BookRentModel.query.get_or_404(rent_id)
        return book_rent

    # @jwt_required()
    def delete(self, rent_id):
        book_rent = BookRentModel.query.get_or_404(rent_id)
        # book = BookModel.
        try:
            db.session.delete(book_rent)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "SQLAlchemyError occurred while deleting BookRental from db.")

        return {"message": "Rent {} successfully deleted".format(rent_id)}

    @blp.arguments(UpdateRentSchema)
    @blp.response(201, PlainRentSchema)
    def put(self, rent_data, rent_id):
        book_rent = BookRentModel.query.get(rent_id)
        book = BookModel.query.get(book_rent.book_id)

        if book_rent:
            book_rent.date_returned = rent_data['date_returned']
            book_rent.status = rent_data['status']
            if rent_data['status'] == 'returned':
                book.status = 'available'
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

    # @jwt_required()
    @blp.arguments(PlainRentSchema)
    @blp.response(201, PlainRentSchema)
    def post(self, rent_data):

        book_rent = BookRentModel(**rent_data)
        book = BookModel.query.get_or_404(rent_data['book_id'])

        if book.status != "available":
            abort(500, "You can not rent this book!")
        else:
            book.status = "rented"

        try:
            db.session.add(book_rent)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "SQLAlchemyError occurred while inserting rental data to db.")

        return book_rent


@blp.route("/rental/client/<int:client_id>")
class ListClientRents(MethodView):

    #todo: modify so that get accepts email in json instead of client id
    # @jwt_required()
    @blp.response(200, PlainRentSchema(many=True))
    def get(self, client_id):

        rentals = BookRentModel.query.filter_by(client_id=client_id).all()

        if not rentals:
            return {"message": "No rents for client with id {}".format(client_id)}
        else:
            return rentals
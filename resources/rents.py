from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import BookRentModel
from schema import PlainRentSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("BookRental", __name__, description="Book rental CRUD.")


@blp.route('/rental/<string:rent_id>')
class BookRental(MethodView):

    def get(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


@blp.route('/rental')
class ListBookRental(MethodView):

    def get(self):
        pass

    def post(self):
        pass
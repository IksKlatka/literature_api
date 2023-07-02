from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from models import BookModel

blp = Blueprint("BooksBlueprint", __name__, description="Books CRUD.")

@blp.route('/book/<string:book_id>')
class Book(MethodView):

    def get(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


@blp.route('/book')
class BookList(MethodView):

    def get(self):
        pass

    def post(self):
        pass
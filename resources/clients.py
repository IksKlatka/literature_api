from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import ClientModel
from schema import PlainClientSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Clients", __name__, description="Clients CRUD.")

@blp.route('/client/<string:client_id>')
class Client(MethodView):

    def get(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

@blp.route('/client')
class ListClient(MethodView):

    def get(self):
        pass

    def post(self):
        pass
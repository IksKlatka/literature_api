from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import ClientModel
from schema import PlainClientSchema, UpdateClientSchema, PlainRentSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256

blp = Blueprint("Clients", __name__, description="Clients CRUD.")


@blp.route('/client/register')
class ClientRegister(MethodView):

    @blp.arguments(PlainClientSchema)
    def post(self, client_data):

        if ClientModel.query.filter(ClientModel.email == client_data['email']).first():
            abort(400, "User with that email already exists.")

        client = ClientModel(
            first_name= client_data['first_name'],
            last_name= client_data['last_name'],
            email = client_data['email'],
            password = pbkdf2_sha256.hash(client_data['password'])
        )

        db.session.add(client)
        db.session.commit()

        return {"message": "Client created!"}, 201


@blp.route('/client/<int:client_id>')
class Client(MethodView):

    @blp.response(200, PlainClientSchema)
    def get(self, client_id):
        client = ClientModel.query.get_or_404(client_id)
        return client

    def delete(self, client_id):
        client = ClientModel.query.get_or_404(client_id)
        try:
            db.session.delete(client)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "SQLAlchemyError occurred while deleting client from db.")

        return {"message": "Client {} successfully deleted".format(client.first_name)}

    @blp.arguments(UpdateClientSchema)
    @blp.response(201, PlainClientSchema)
    def put(self, client_data, client_id):

        client = ClientModel.query.get(client_id)

        if client:
            client.first_name = client_data.get("first_name", client.first_name)
            client.last_name = client_data.get("last_name", client.last_name)
            client.email = client_data.get("email", client.email)
        else:
            client = ClientModel(id=client_id, **client_data)

        db.session.add(client)
        db.session.commit()

        return client
@blp.route('/client')
class ListClient(MethodView):

    @blp.response(200, PlainClientSchema(many=True))
    def get(self):
        return ClientModel.query.all()

    # @blp.arguments(PlainClientSchema)
    # @blp.response(201, PlainClientSchema)
    # def post(self, client_data):
    #     client = ClientModel(**client_data)
    #
    #     try:
    #         db.session.add(client)
    #         db.session.commit()
    #     except SQLAlchemyError:
    #         abort(500, "SQLAlchemyError occurred while inserting client to db.")
    #
    #     return client



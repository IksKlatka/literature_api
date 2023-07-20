from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (jwt_required,
                                create_access_token,
                                get_jwt,
                                get_jwt_identity,
                                create_refresh_token)
from flask import jsonify
from db import db
from blocklist import BLOCKLIST
from models import ClientModel, ClientRoleModel, RoleModel, check_permissions
from schema import PlainClientSchema, UpdateClientSchema, LoginClientSchema
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

@blp.route('/client/login')
class ClientLogin(MethodView):

    @blp.arguments(LoginClientSchema)
    def post(self, client_data):
        client = ClientModel.query.filter(ClientModel.email == client_data['email']).first()

        if client and pbkdf2_sha256.verify(client_data['password'], client.password):
            access_token = create_access_token(identity=client.id)
            refresh_token = create_refresh_token(identity=client.id)
            return {"access token": access_token,
                    "refresh token": refresh_token}, 200

        abort(401, "Invalid client data.")

@blp.route('/client/logout')
class ClientLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out!"}, 200

@blp.route('/client/refresh')
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"access token": create_access_token(identity=get_jwt_identity(), fresh=False)}
        # note: jwt_identity == identity of current client as we use client_id in out jwts

@blp.route('/client/<int:client_id>')
class Client(MethodView):

    @blp.response(200, PlainClientSchema)
    def get(self, client_id):
        client = ClientModel.query.get_or_404(client_id)
        return client

    # @jwt_required()
    def delete(self, client_id):
        client = ClientModel.query.get_or_404(client_id)
        try:
            db.session.delete(client)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "SQLAlchemyError occurred while deleting client from db.")

        return {"message": "Client {} successfully deleted".format(client.first_name)}

    # @jwt_required() #note: fresh=True - EMBRACE IT!
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

    @jwt_required()
    @blp.response(200, PlainClientSchema(many=True))
    def get(self):
        c_client = get_jwt_identity()
        if check_permissions(c_client):
            return ClientModel.query.all()
        return (
            jsonify({"message": "Lack of permissions."})
        )






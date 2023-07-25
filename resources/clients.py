from flask.views import MethodView
from flask_smorest import Blueprint, abort
import flask_jwt_extended as jwt
from flask import jsonify
from db import db
from blocklist import BLOCKLIST
from models import (ClientModel,
                    ClientRoleModel,
                    RoleModel,
                    check_admins_permissions,
                    check_superadmin_permissions)
from schema import (PlainClientSchema,
                    UpdateClientSchema,
                    LoginClientSchema,
                    AdminFromClientSchema,
                    ClientRoleSchema)
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

        client = ClientModel.query.get_or_404(client.id)
        client_role = ClientRoleModel(client_id =client.id, role_id=3)

        db.session.add(client_role)
        db.session.commit()
        return {"message": "Client created!"}, 201

@blp.route('/client/login')
class ClientLogin(MethodView):

    @blp.arguments(LoginClientSchema)
    def post(self, client_data):
        client = ClientModel.query.filter(ClientModel.email == client_data['email']).first()

        if client and pbkdf2_sha256.verify(client_data['password'], client.password):
            access_token = jwt.create_access_token(identity=client.id)
            refresh_token = jwt.create_refresh_token(identity=client.id)
            return {"access token": access_token,
                    "refresh token": refresh_token}, 200

        abort(401, "Invalid client data.")

@blp.route('/client/logout')
class ClientLogout(MethodView):
    @jwt.jwt_required()
    def post(self):
        jti = jwt.get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out!"}, 200


@blp.route('/client/refresh')
class RefreshToken(MethodView):
    @jwt.jwt_required(refresh=True)
    def post(self):
        jti = jwt.get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"access token": jwt.create_access_token(identity=jwt.get_jwt_identity(), fresh=False)}
        # note: jwt_identity == identity of current client as we use client_id in out jwts

@blp.route('/client/<int:client_id>')
class Client(MethodView):

    @blp.response(200, PlainClientSchema)
    def get(self, client_id):
        client = ClientModel.query.get_or_404(client_id)
        return client

    @jwt.jwt_required()
    def delete(self, client_id):
        if check_admins_permissions(jwt.get_jwt_identity()):
            client = ClientModel.query.get_or_404(client_id)
            db.session.delete(client)
            db.session.commit()
            return {"message": "Client {} successfully deleted".format(client.first_name)}
        return jsonify({"message": "Lack of permissions."}), 403


    @jwt.jwt_required() #note: fresh=True - EMBRACE IT!
    @blp.arguments(UpdateClientSchema)
    @blp.response(201, PlainClientSchema)
    def put(self, client_data, client_id):

        if client_id == jwt.get_jwt_identity():
            client = ClientModel.query.get(client_id)
            if client:
                client.first_name = client_data.get("first_name", client.first_name)
                client.last_name = client_data.get("last_name", client.last_name)
                client.email = client_data.get("email", client.email)
            else:
                client = ClientModel(id=client_id, **client_data)

            db.session.add(client)
            db.session.commit()
            return jsonify({"message": f"Client {client.id} updated successfully."})
        return jsonify({"message": "Lack of permissions."})




@blp.route('/client')
class ListClient(MethodView):

    @jwt.jwt_required()
    @blp.response(200, PlainClientSchema(many=True))
    def get(self):
        c_client = jwt.get_jwt_identity()
        if check_admins_permissions(c_client):
            return ClientModel.query.all()
        return (
            jsonify({"message": "Lack of permissions."})
        )

@blp.route('/client/role')
class ListClientRole(MethodView):

    @jwt.jwt_required()
    @blp.response(200, ClientRoleSchema(many=True))
    def get(self):
        c_client = jwt.get_jwt_identity()
        if check_admins_permissions(c_client):
            return ClientRoleModel.query.all()
        return jsonify({"message": "Lack of permissions."})


    @jwt.jwt_required()
    @blp.arguments(AdminFromClientSchema)
    @blp.response(201, ClientRoleModel)
    def put(self, admin_data):

        if check_superadmin_permissions(jwt.get_jwt_identity()):
            client = ClientModel.query.filter_by(id=admin_data['client_id']).first()
            role = RoleModel.query.filter_by(id=admin_data['role_id']).first()
            if client and role:

                past_role = ClientRoleModel.query.filter_by(client_id=admin_data['client_id']).first()
                db.session.delete(past_role)

                client_role = ClientRoleModel(
                    client_id = admin_data['client_id'],
                    role_id = admin_data['role_id'])

                db.session.add(client_role)
                db.session.commit()
                return jsonify({"message": f"Client {client_role} updated to admin successfully."})
        return jsonify({"message": "Lack of permissions."})

@blp.route('/client/<int:client_id>/role')
class ClientRole(MethodView):

    @jwt.jwt_required()
    @blp.response(200, ClientRoleSchema)
    def get(self, client_id):

        client = jwt.get_jwt_identity()
        if client == client_id:
            role = RoleModel.query.join(ClientRoleModel, ClientRoleModel.role_id == RoleModel.id) \
                .filter(ClientRoleModel.client_id == client_id).first()

            return jsonify({"message": f"Your role: {role.name}"})
        return jsonify({"message": f"You can only check your role. Your ID is {client}."})
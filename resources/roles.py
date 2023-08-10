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

blp = Blueprint("Roles", __name__, "CRUD on Roles.")



@blp.route('/role/<int:client_id>')
class ListClientRole(MethodView):

    @jwt.jwt_required()
    @blp.response(200, ClientRoleSchema)
    def get(self, client_id):

        client = jwt.get_jwt_identity()

        if client == client_id or check_admins_permissions(client):
            client_role = ClientRoleModel.query.filter_by(client_id=client_id).first()
            return client_role
        else:
            return jsonify({"message": "Lack of permissions."})


@blp.route('/role')
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
        """
        Enabled only for SuperAdmin.
        Upgrade Client to Admin or SuperAdmin
        :return: 201
        """

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

                new_role = RoleModel.query.get(admin_data['role_id'])

                return jsonify({"message": f"Client {client_role.client_id} updated to {new_role.name} successfully."})
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
from db import db


class ClientModel(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), unique=False, nullable=True)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # role_id = db.Column(db.Integer, default= 3, unique=False, nullable=False)
    book_rent = db.relationship("BookRentModel", back_populates="client",
                                lazy="dynamic")

    roles = db.relationship("RoleModel", secondary="client_roles", back_populates="clients")


class RoleModel(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    tag = db.Column(db.String, unique=True, nullable=False)

    clients = db.relationship("ClientModel", secondary="client_roles", back_populates="roles")


class ClientRoleModel(db.Model):
    __tablename__ = "client_roles"

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)


def check_admins_permissions(client_id: int) -> bool:
    if ClientModel.query.filter(ClientModel.id == client_id).join(ClientModel.roles). \
            filter(RoleModel.tag == "admin" or RoleModel.tag == "super_admin"):
        return True
    return False

def check_superadmin_permissions(client_id: int) -> bool:
    if ClientModel.query.filter(ClientModel.id == client_id).join(ClientModel.roles). \
            filter(RoleModel.tag == "super_admin"):
        return True
    return False


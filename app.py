import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST
from resources.books import blp as BooksBlueprint
from resources.countries import blp as CountriesBlueprint
from resources.rents import blp as RentalBlueprint
from resources.clients import blp as ClientBlueprint
from resources.roles import blp as RoleBlueprint


def create_app(db_url= None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "CountryLiterature REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", None)

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST

    @jwt.revoked_token_loader   #note: callback - return message
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "Token has been revoked!",
                     "error": "token_revoked"}),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired!", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": "Token verification failed!", "error": "invalid_token"}),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"message": "Access token not provided!", "error": "unauthorized_loader"}),
            401,
        )

    api.register_blueprint(BooksBlueprint)
    api.register_blueprint(CountriesBlueprint)
    api.register_blueprint(RentalBlueprint)
    api.register_blueprint(ClientBlueprint)
    api.register_blueprint(RoleBlueprint)


    return app


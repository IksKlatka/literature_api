from flask import Flask
from db import db
from flask_smorest import Api
import os
from resources.books import blp as BooksBlueprint
from resources.countries import blp as CountriesBlueprint
from resources.rents import blp as RentalBlueprint
from resources.clients import blp as ClientBlueprint


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

    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(BooksBlueprint)
    api.register_blueprint(CountriesBlueprint)
    api.register_blueprint(RentalBlueprint)
    api.register_blueprint(ClientBlueprint)


    return app


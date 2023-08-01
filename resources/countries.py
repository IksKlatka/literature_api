from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import jsonify
import flask_jwt_extended as jwt
from db import db
from models import CountryModel, check_admins_permissions, check_superadmin_permissions
from schema import CountrySchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Countries", __name__, description="Countries CRUD.")

@blp.route('/country/<string:country_id>')
class Country(MethodView):
    @blp.response(200, CountrySchema)
    def get(self, country_id):
        country = CountryModel.query.get_or_404(country_id)
        return country

    @jwt.jwt_required()
    def delete(self, country_id):

        if check_admins_permissions(jwt.get_jwt_identity()):
            country = CountryModel.query.get_or_404(country_id)
            db.session.delete(country)
            db.session.commit()
            return (
                jsonify({"message": "Country {} successfully deleted.".format(country.name)}),
                200
            )
        return {"message": "Lack of permissions."}

    @jwt.jwt_required()
    @blp.arguments(CountrySchema)
    @blp.response(201, CountrySchema)
    def put(self, country_data, country_id):

        if check_admins_permissions(jwt.get_jwt_identity()):

            country = CountryModel.query.get(country_id)
            if country:
                country.name = country_data['name']
                country.continent = country_data['continent']
            else:
                country = CountryModel(id= country_id, **country_data)
            db.session.add(country)
            db.session.commit()

            return jsonify({"message": f"Country {country_data['name']} updated successfully."}), 201

        return (
            jsonify({"message": "Lack of permissions."})
        )

@blp.route('/country')
class CountriesList(MethodView):

    @blp.response(200, CountrySchema(many=True))
    def get(self):
        return CountryModel.query.all()

    @jwt.jwt_required()
    @blp.arguments(CountrySchema)
    @blp.response(201, CountrySchema)
    def post(self, country_data):

        if check_admins_permissions(jwt.get_jwt_identity()):

            country = CountryModel(**country_data)
            db.session.add(country)
            db.session.commit()
            return jsonify({"message": f"Country {country.name} successfully created."})
        return (
            jsonify({"message": "Lack of permissions."})
        )
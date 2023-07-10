from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from models import CountryModel
from schema import CountrySchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Countries", __name__, description="Countries CRUD.")

@blp.route('/country/<string:country_id>')
class Country(MethodView):
    @blp.response(200, CountrySchema)
    def get(self, country_id):
        country = CountryModel.query.get_or_404(country_id)
        return country

    def delete(self, country_id):
        country = CountryModel.query.get_or_404(country_id)
        db.session.delete(country)
        db.session.commit()
        return {"message": "Country {} successfully deleted.".format(country.name)}

    @blp.arguments(CountrySchema)
    @blp.response(201, CountrySchema)
    def put(self, country_data, country_id):
        country = CountryModel.query.get(country_id)

        if country:
            country.name = country_data['name']
            country.continent = country_data['continent']
        else:
            country = CountryModel(id= country_id, **country_data)

        db.session.add(country)
        db.session.commit()

        return country

@blp.route('/country')
class CountriesList(MethodView):

    @blp.response(200, CountrySchema(many=True))
    def get(self):
        return CountryModel.query.all()

    @blp.arguments(CountrySchema)
    @blp.response(201, CountrySchema)
    def post(self, country_data):

        country = CountryModel(**country_data)

        try:
            db.session.add(country)
            db.session.commit()
        except IntegrityError:
            abort(400, "Country already exists.")
        except SQLAlchemyError:
            abort(500, "SQLAlchemyError occurred while inserting country.")\

        return country
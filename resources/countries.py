from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from models import CountryModel

blp = Blueprint("CountriesBlueprint", __name__, description="Books CRUD.")

@blp.route('/country/<string:country_id>')
class Country(MethodView):

    def get(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


@blp.route('/country')
class CountriesList(MethodView):

    def get(self):
        pass

    def post(self):
        pass
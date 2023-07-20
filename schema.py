from marshmallow import Schema, fields, validate
from sqlalchemy import Enum

#todo: create schemas for roles and client_roles
class PlainBookSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    genre = fields.String(required=False)
    year_published = fields.Integer(required=False)
    status = fields.String(required=False, validate=validate.OneOf(['available',
                                                                    'rented']))

class PlainCountrySchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    continent = fields.String(required=True)

class UpdateBookSchema(Schema):
    title = fields.String(required=True)
    author = fields.String(required=True)
    genre = fields.String(required=False)
    year_published = fields.Integer(required=False)
    status = fields.String(required=False, validate=validate.OneOf(['available',
                                                                    'rented']))
    country_id = fields.Integer(required=False)

class BookSchema(PlainBookSchema):
    country_id = fields.Integer(required=True, load_only=True)
    country = fields.Nested(PlainCountrySchema(), dump_only=True)

class CountrySchema(PlainCountrySchema):
    books = fields.List(fields.Nested(PlainBookSchema()), dump_only=True)

class PlainClientSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=False)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

class UpdateClientSchema(Schema):
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    email = fields.String(required=False)

class LoginClientSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

class PlainRentSchema(Schema):
    id = fields.Integer(dump_only=True)
    book_id = fields.Integer(required=True)
    client_id = fields.Integer(required=True)
    date_rented = fields.Date(required=True)
    date_returned = fields.Date(required=False)
    status = fields.String(required=True, validate=validate.OneOf(['rented',
                                                                   'delayed',
                                                                   'extended']))

class UpdateRentSchema(Schema):
    date_returned = fields.Date(required=True)
    status = fields.String(required=True, validate=validate.OneOf(['returned',
                                                                   'delayed',
                                                                   'extended']))


from marshmallow import Schema, fields, validate
from sqlalchemy import Enum

class PlainBookSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    genre = fields.String(required=False)
    year_published = fields.Integer(required=False)
    status = fields.String(required=False, validate=validate.OneOf(['available',
                                                                    'rented']))

# note: UpdateCountry is same as PlainCountry that's why it doesn't exist
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

class AdminFromClientSchema(Schema):
    client_id = fields.Integer(required=True)
    role_id = fields.Integer(required=True)
class LoginClientSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

class UpdateClientSchema(Schema):
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    email = fields.String(required=False)

class RoleSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    tag = fields.String(required=True)

class ClientRoleSchema(Schema):
    client_id = fields.Integer(dump_only=True)
    role_id = fields.Integer(dump_only=True)



class PlainRentSchema(Schema):
    id = fields.Integer(dump_only=True)
    book_id = fields.Integer(required=True)
    client_id = fields.Integer(required=True)
    date_rented = fields.Date(required=True)
    date_returned = fields.Date(required=False)
    status = fields.String(required=True, validate=validate.OneOf(['rented',
                                                                   'delayed',
                                                                   'extended']))

    books = fields.Nested(PlainBookSchema())


class UpdateRentSchema(Schema):
    date_returned = fields.Date(required=True)
    status = fields.String(required=True, validate=validate.OneOf(['returned',
                                                                   'delayed',
                                                                   'extended']))


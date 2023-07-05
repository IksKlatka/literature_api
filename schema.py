from marshmallow import Schema, fields, validate


class PlainBookSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    genre = fields.String(required=False)
    year_published = fields.Integer(required=False)

class PlainCountrySchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    continent = fields.String(required=True)

class UpdateBookSchema(Schema):
    title = fields.String(required=True)
    author = fields.String(required=True)
    genre = fields.String(required=False)
    year_published = fields.Integer(required=True)
    country_id = fields.Integer()


class BookSchema(PlainBookSchema):
    country_id = fields.Integer(required=True, load_only=True)
    country = fields.Nested(PlainCountrySchema(), dump_only=True)

class CountrySchema(PlainCountrySchema):
    books = fields.List(fields.Nested(PlainBookSchema()), dump_only=True)

class PlainClientSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)

class UpdateClientSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)

class PlainRentSchema(Schema):
    id = fields.Integer(dump_only=True)
    book_id = fields.Integer(required=True)
    client_id = fields.Integer(required=True)
    date_rented = fields.Date(required=True)
    date_returned = fields.Date(required=False)
    status = fields.String(validate=validate.OneOf(['rented', 'extended', 'returned']), required=True)

class UpdateRentSchema(Schema):
    date_returned = fields.Date(required=True)
    status = fields.String(validate=validate.OneOf(['rented', 'extended', 'returned']), required=True)

# class RentSchema(PlainRentSchema):
#     book_id = fields.Integer(required=True, load_only=True)
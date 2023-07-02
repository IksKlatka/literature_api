from marshmallow import Schema, fields


class PlainBookSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    year_published = fields.Date(required=False)

class PlainCountrySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    continent = fields.String(required=True)

class UpdateBookSchema(Schema):
    pass

class BookSchema(Schema):
    pass

class CountrySchema(Schema):
    pass
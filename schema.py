from marshmallow import Schema, fields


class PlainBookSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    year_published = fields.Integer(required=False)

class PlainCountrySchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    continent = fields.String(required=True)

class UpdateBookSchema(Schema):
    title = fields.String(required=True)
    author = fields.String(required=True)
    year_published = fields.Integer(required=True)
    country_id = fields.Integer()


class BookSchema(PlainBookSchema):
    country_id = fields.Integer(required=True, load_only=True)
    country = fields.Nested(PlainCountrySchema(), dump_only=True)

class CountrySchema(PlainCountrySchema):
    books = fields.List(fields.Nested(PlainBookSchema()), dump_only=True)
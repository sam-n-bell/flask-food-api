from marshmallow import Schema, fields
from marshmallow.validate import Length, Range

class CreateFoodInputSchema(Schema):
    name = fields.Str(required=True, validate=Length(min=1))
    calories = fields.Int(required=True, validate=Range(min=0))


def return_errors_str(errors):
    errors_str = ''
    for k, v in errors.items():
        errors_str += str(k)
        errors_str += ': '
        for error in v:
            errors_str += error
            errors_str += ' '
    return errors_str


import json
from rest_framework.fields import Field

class RawJsonField(Field):
    """
    This field renders a text directly as JSON in the API.
    If the string is no JSON it returns an empty JSON object.
    """
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        try:
            return json.loads(value)
        except ValueError as e:
            return {}

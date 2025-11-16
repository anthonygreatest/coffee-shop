


class Validations:

    def validate_response(self, response, schema):
        if isinstance(response, list):
            try:
                for item in response:
                    schema.model_validate(item)
            except Exception:
                raise Exception('Wrong format')

        else:
            try:
                schema.model_validate(response.json())
            except Exception:
                raise Exception('Wrong format')

    def validate_response_from_order(self, response, schema, subschema):

        if isinstance(response, list):
            try:
                for member in response:
                    schema.model_validate(member)
                    for item in member['products']:
                        subschema.model_validate(item)
            except Exception:
                raise Exception('Wrong order format')
        else:
            try:
                schema.model_validate(response)
                for item in response['products']:
                    subschema.model_validate(item)
            except Exception:
                raise Exception('Wrong order format')

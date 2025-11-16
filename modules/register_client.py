


class RegisterModule:

    def prepare_data(self, data, schema):
        checked_data = schema(
            email=data.email
        )
        return checked_data.model_dump_json()
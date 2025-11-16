

class CreateOrderModule:

    def data_molder(self, data, schema, subschema):

        data['products'] = [subschema(**product) for product in data['products']]

        return schema(**data).model_dump_json()
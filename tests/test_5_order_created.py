import json
from http import HTTPStatus

from utils.schemas.order_created_schema import InsideOrderCreatedSchema, OrderCreatedSchema



def test_order_created(create_order, assertion, validation):

    clients_request, clients_response, status_codes = create_order

    assertion.assert_response_status_code(
        response=status_codes,
        expected=HTTPStatus.CREATED
    )
    validation.validate_response_from_order(
        response=clients_response,
        schema=OrderCreatedSchema,
        subschema=InsideOrderCreatedSchema
    )

def test_order_fields(create_order, assertion, validation):

    clients_request, clients_response, _ = create_order

    # request_data_dict = json.loads(request_data)

    assertion.assert_orders_response(
        response=clients_response,
        request=clients_request
    )


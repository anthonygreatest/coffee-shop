import random
from http import HTTPStatus


from utils.schemas.order_created_schema import OrderCreatedSchema, InsideOrderCreatedSchema


def test_get_order_by_id(api_client, create_order, token_from_client, assertion, validation):
    headers, _ = token_from_client

    _, clients_response, _ = create_order

    resp_from_orders = random.choice(clients_response)
    print(resp_from_orders)

    resp = api_client.get_order_by_id(
        id=resp_from_orders['id'],
        headers=headers
    )

    validation.validate_response_from_order(
        response=resp.json(),
        schema=OrderCreatedSchema,
        subschema=InsideOrderCreatedSchema
    )

    assertion.assert_orders_response(
        response=resp,
        request=resp_from_orders
    )

def test_get_order_by_id_status_code(api_client, create_order, token_from_client, assertion):
    headers, _ = token_from_client

    _, clients_response, _ = create_order

    resp_from_orders = random.choice(clients_response)

    resp = api_client.get_order_by_id(
        id=resp_from_orders['id'],
        headers=headers
    )

    assertion.assert_response_status_code(
        response=resp,
        expected=HTTPStatus.OK
    )

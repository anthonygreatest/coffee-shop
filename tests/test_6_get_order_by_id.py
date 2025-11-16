import json
import random
from http import HTTPStatus

import allure

from utils.schemas.order_created_schema import OrderCreatedSchema, InsideOrderCreatedSchema

@allure.story('Getting order by ID')
def test_get_order_by_id(api_client, create_order, token_from_client, assertion, validation):
    headers, _ = token_from_client

    _, clients_response, _ = create_order

    resp_from_orders = random.choice(clients_response)

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

    allure.attach(
        json.dumps(resp.json(), indent=2),
        name='Selected order by ID',
        attachment_type=allure.attachment_type.JSON
    )

@allure.story('Getting order by ID')
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


    allure.attach(
        body=str(resp.status_code),
        name='Response code: order selected by ID',
        attachment_type=allure.attachment_type.TEXT
    )
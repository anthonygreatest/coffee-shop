import json
from http import HTTPStatus

import allure

from utils.schemas.order_created_schema import InsideOrderCreatedSchema, OrderCreatedSchema


@allure.story('Creating Order')
def test_order_created(create_order, assertion, validation):

    with allure.step('Check creating order'):

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

@allure.story('Creating Order')
def test_order_fields(create_order, assertion, validation):

    with allure.step('Checking orders created match'):
        clients_request, clients_response, _ = create_order

        assertion.assert_orders_response(
            response=clients_response,
            request=clients_request
        )

        for order in clients_response:
            allure.attach(
                json.dumps(order, indent=2),
                name='Orders in Response',
                attachment_type=allure.attachment_type.JSON
            )

        for order in clients_request:
            allure.attach(
                json.dumps(order, indent=2),
                name='Orders in Request',
                attachment_type=allure.attachment_type.JSON
            )




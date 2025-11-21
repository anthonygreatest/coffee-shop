import json
from dataclasses import dataclass
from http import HTTPStatus

import allure
from sqlalchemy import text

from tests.helpers import tuple_handler
from utils.schemas.order_created_schema import InsideOrderCreatedSchema, OrderCreatedSchema
from utils.tables import Orders, OrderItems


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



def test_orders_added_to_db(create_order, get_db_session, assertion):

    clients_request, clients_response, _ = create_order

    check_order_in_db = (get_db_session.query(OrderItems.order_id, Orders.clientId, OrderItems.created, Orders.customer_name, OrderItems.product_id, OrderItems.quantity).
                         join(OrderItems, Orders.id == OrderItems.order_id).order_by('created').all())


    resp_from_db = tuple_handler(check_order_in_db)

    assertion.assert_orders_response(clients_response, resp_from_db)

    print(resp_from_db)
    print(clients_response)


def test_orders_in_kafka(create_order, kafka_consumer):

    clients_request, clients_response, _ = create_order

    messages = []

    consumer = kafka_consumer('orders_at_coffee_shop')

    while True:
        msg = consumer.poll(timeout_ms=300)
        if not msg:  # пустой словарь {}
            break
        for _, records in msg.items():
            for record in records:
                messages.append(record.value)

    for item in clients_response:
        assert item in messages
        print(item)

    print(messages)



# def test_delete_order_from_db(create_order, get_db_session, assertion): необязательный т.к нет ручки
#
#     clients_request, clients_response, _ = create_order
#
#     check_order_in_db = (get_db_session.query(OrderItems.order_id, Orders.clientId, OrderItems.created, Orders.customer_name, OrderItems.product_id, OrderItems.quantity).
#                          join(OrderItems, Orders.id == OrderItems.order_id).order_by('created').all())
#
#
#     resp_from_db = tuple_handler(check_order_in_db)
#
#     order_ids = [i['id'] for i in resp_from_db]
#     orders_to_delete = get_db_session.query(Orders).filter(Orders.id.in_(order_ids))
#
#     for order in orders_to_delete:
#         get_db_session.delete(order)
#         get_db_session.commit()
#
#     check_order_in_db_after_delete = (
#         get_db_session.query(OrderItems.order_id, Orders.clientId, OrderItems.created, Orders.customer_name,
#                              OrderItems.product_id, OrderItems.quantity).
#         join(OrderItems, Orders.id == OrderItems.order_id).order_by('created').all())
#
#     assert len(check_order_in_db_after_delete) == 0






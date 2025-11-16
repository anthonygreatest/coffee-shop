import allure

from utils.schemas.get_all_orders_schema import GetAllOrdersSchema


@allure.story('Getting all orders')
def test_get_all_orders(get_all_orders, create_order, validation):

    _, clients_response, _ = create_order

    validation.validate_response(
        response=get_all_orders.json(),
        schema=GetAllOrdersSchema
    )

    get_all_orders = sorted(get_all_orders.json(), key=lambda x: x['created'])

    allure.attach(
        body=str(get_all_orders),
        name='All orders received',
        attachment_type=allure.attachment_type.TEXT
    )

    for i in range(len(clients_response)):

        assert clients_response[i]['created'] == get_all_orders[i]['created']

        assert clients_response[i]['customerName'] == get_all_orders[i]['customerName']

        assert clients_response[i]['id'] == get_all_orders[i]['id']

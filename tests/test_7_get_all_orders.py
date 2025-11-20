import allure

from tests.conftest import get_db_session
from tests.helpers import tuple_handler2
from utils.schemas.get_all_orders_schema import GetAllOrdersSchema
from utils.tables import Orders, OrderItems


@allure.story('Getting all orders')
def test_get_all_orders(get_all_orders, create_order, validation, get_db_session):

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


@allure.story('Getting all orders')
def test_get_all_orders_from_db(get_all_orders, create_order, validation, get_db_session):

    _, clients_response, _ = create_order

    get_all_orders = sorted(get_all_orders.json(), key=lambda x: x['created'])

    a = (get_db_session.query(Orders.id, OrderItems.created, Orders.customer_name).
     join(OrderItems, Orders.id == OrderItems.order_id).order_by('created')).all()

    print(a)

    from_db = tuple_handler2(a)

    for i in range(len(get_all_orders)):

        assert get_all_orders[i]['customerName'] == from_db[i]['customerName']

        assert get_all_orders[i]['id'] == from_db[i]['id']

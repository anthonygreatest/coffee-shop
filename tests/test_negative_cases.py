import json
import random
from http import HTTPStatus
from random import randrange

import allure
import pytest
import requests

from data.constants import CATEGORIES, PRODUCT_IDS

from data.dataclasses.products import Products
from data.endpoints import Endpoints
from modules.create_order import CreateOrderModule

from utils.schemas.create_order_schema import InsideProductsSchema, CreateOrderSchema
from utils.schemas.register_request_schema import RegisterRequestSchema


@pytest.mark.parametrize(
    'page, number',
    [
        (1011, 0),
        (-100, 0),
        ('abc', 0),
        (9999999, 0),
        (1, 10)
    ]
)
@allure.story('Nonexistent pages')
def test_nonexistent_page(api_client, page, number):
    with allure.step('Nonexistent pages'):
        params = Products(
            category=random.choice(CATEGORIES),
            page=page
        )

        resp = api_client.get_products(
            data=params
        )

    assert len(resp.json()['products']) == number

@pytest.mark.parametrize(
    'category_product, number',
    [
        (1011, 0),
        ("sandwiches", 0),
        ('abc', 0),
        ('@@', 0),
        ("", 0),
        ("/*", 0)

    ]
)
def test_nonexistent_cat(api_client, category_product, number):
    params = Products(
        category=category_product,
    )

    resp = api_client.get_products(
        data=params
    )
    assert len(resp.json()['products']) == number


@pytest.mark.parametrize(
    'category_input', [
        "'; DROP TABLE products; --",
        "/*",
        "abc' OR '1'='1",
        "\" OR \"\"=\"",
        "<script>alert(1)</script>"
    ]
)
def test_sql_injection(api_client, category_input):

    params = Products(
        category=category_input,
        page=1
    )

    resp = api_client.get_products(
        data=params
    )

    assert resp.status_code in [200, 400, 404]

    assert resp.status_code != 500

@pytest.mark.parametrize(
    'limit, number',
    [
        (1011, 33),
        ("sandwiches", 0),
        ('abc', 0),
        ('@@', 0),
        (33, 33),
        (9999999, 0),
        (1, 1),
        (max, 33)
    ]
)
def test_nonexistent_limit(api_client, limit, number):
    params = Products(
        limit=limit
    )

    resp = api_client.get_products(
        data=params
    )
    assert len(resp.json()['products']) == number

def test_wrong_method():
    params = Products(
        category='cookie',
        limit=1,
        page=1
    )

    params2 = {key: value for key, value in params.__dict__.items()}

    print(params)
    resp = requests.post(
        url=f'{Endpoints().BASE_URL}{Endpoints().PRODUCTS}',
        data=json.dumps(params2)
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.parametrize(
    'id_product, res',
    [
        (1011, HTTPStatus.NOT_FOUND),
        (5001, HTTPStatus.NOT_FOUND),
        ('abc', HTTPStatus.BAD_REQUEST),
        (-100, HTTPStatus.NOT_FOUND),
        (0, HTTPStatus.NOT_FOUND),
        ('@!#', HTTPStatus.NOT_FOUND)
    ]
)
def test_nonexistent_product(api_client, id_product, res):

    resp = api_client.get_single_product(
            product_id=id_product
    )

    assert resp.status_code == res


@pytest.mark.parametrize(
    'email, res', [
        ('walterwhitemail.ru', HTTPStatus.BAD_REQUEST),
        ('tony', HTTPStatus.BAD_REQUEST),
        (12345, HTTPStatus.BAD_REQUEST),
        ('', HTTPStatus.BAD_REQUEST),
        ('@!walter', HTTPStatus.BAD_REQUEST),
        (True, HTTPStatus.BAD_REQUEST),
        ('haljamesincandenzaisafictionalcharactercreatedbydavidfosterwallaceandthisishisschoolemail@gmail.com', HTTPStatus.BAD_REQUEST)
    ]
)
def test_register_invalid_user(api_client, token_from_client, email, res):

    resp = api_client.register_client(
        data=email
    )

    assert resp.status_code == res

def test_register_user_without_body(api_client):

    resp = api_client.register_client(
        data=None
    )

    assert resp.status_code == HTTPStatus.BAD_REQUEST

def test_register_user_again(api_client, email_generator, register_module):

    email = register_module.prepare_data(
        data=email_generator,
        schema=RegisterRequestSchema
    )

    headers = {
         'Content-Type': 'application/json'
    }

    resp = api_client.register_client(
        data=email,
        headers=headers
    )

    resp2 = api_client.register_client(
        data=email,
        headers=headers
    )
    assert resp2.json()['error'] == 'Email already registered'


def test_create_order_without_token(api_client, order_generator, register_module):

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
            'customerName': order_generator.customerName,
            'products': [p.__dict__ for p in order_generator.products]
    }

    resp = api_client.create_order(
        data=CreateOrderModule().data_molder(data, CreateOrderSchema, InsideProductsSchema),
        headers=headers
    )

    assert resp.json()['error'] == "Missing API key"
    print(resp.json())


@pytest.mark.parametrize(
    'data, quant, res', [
        (500,  randrange(1, 10), HTTPStatus.BAD_REQUEST),
        (0, randrange(1, 10), HTTPStatus.BAD_REQUEST),
        ('1', randrange(1, 10), HTTPStatus.BAD_REQUEST),
        ('abc', randrange(1, 10), HTTPStatus.BAD_REQUEST),
        ('', randrange(1, 10), HTTPStatus.BAD_REQUEST),
        ("a", randrange(1, 10), HTTPStatus.BAD_REQUEST),
        (random.choice(PRODUCT_IDS), 0, HTTPStatus.BAD_REQUEST),
        (random.choice(PRODUCT_IDS), -1, HTTPStatus.BAD_REQUEST),
        (random.choice(PRODUCT_IDS), 'abc', HTTPStatus.BAD_REQUEST),
        (random.choice(PRODUCT_IDS), '', HTTPStatus.BAD_REQUEST),
        (random.choice(PRODUCT_IDS), '@', HTTPStatus.BAD_REQUEST),
        (random.choice(PRODUCT_IDS), randrange(1, 10), HTTPStatus.CREATED)

    ]
)
def test_invalid_products_for_order(api_client, data, res, quant, token_from_client, order_generator):

    headers, _ = token_from_client

    body_to_send = {
        "customerName":order_generator.customerName,
        "products": [{
            "id": data,
            "quantity": quant
        }]
    }

    resp = api_client.create_order(
        data=json.dumps(body_to_send),
        headers=headers
    )
    print(resp.json())
    assert resp.json()['error'] == 'Invalid, unavailable, or zero-quantity products found'

def test_create_order_with_get_method(api_client, order_generator, register_module, token_from_client):

    headers, _ = token_from_client

    data = {
        'customerName': order_generator.customerName,
        'products': [p.__dict__ for p in order_generator.products]
    }

    resp = requests.get(
            url=f'{Endpoints().BASE_URL}{Endpoints().ORDERS}',
            data=json.dumps(data),
            headers=headers)

    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_create_order_again(api_client, token_from_client, order_generator):

    headers, _ = token_from_client

    body_to_send = {
        "customerName": order_generator.customerName,
        "products": [{
            "id": random.choice(PRODUCT_IDS),
            "quantity": randrange(1, 10)
        }]
    }

    resp = api_client.create_order(
        data=json.dumps(body_to_send),
        headers=headers
    )

    resp2 = api_client.create_order(
        data=body_to_send,
        headers=headers
    )

    assert resp2.status_code == HTTPStatus.BAD_REQUEST






@pytest.mark.parametrize(
    'order_id, res', [
        (1000, HTTPStatus.NOT_FOUND),
        ('abc', HTTPStatus.NOT_FOUND),
        ('', HTTPStatus.NOT_FOUND),
    ]
)
def test_order_by_wrong_id(api_client, token_from_client, order_id, res):
    headers, _ = token_from_client

    resp = api_client.get_order_by_id(
        id=order_id,
        headers=headers
    )
    print(resp.json())

    assert resp.status_code == res

def test_order_by_id_without_token(api_client, create_order):

    headers = {
        'Content-Type': 'application/json'
    }

    _, clients_response, _ = create_order

    resp_from_orders = random.choice(clients_response)

    resp = api_client.get_order_by_id(
        id=resp_from_orders,
        headers=headers
    )

    assert resp.status_code == HTTPStatus.UNAUTHORIZED

def test_get_all_orders_without_token(api_client, create_order, token_from_client):

    headers = {
        'Content-Type': 'application/json'
    }

    resp = api_client.get_all_orders(
        headers=headers
    )

    assert resp.status_code == HTTPStatus.UNAUTHORIZED





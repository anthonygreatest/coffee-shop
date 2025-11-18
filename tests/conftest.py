import json
import random
import time

import pytest

from data.constants import CATEGORIES
from data.dataclasses.products import Products
from data.generator.builder import OrderBuilder
from data.generator.generator import Generator
from modules.create_order import CreateOrderModule
from modules.register_client import RegisterModule
from utils.api_client import APIClient
from utils.assertions import Assertions
from utils.schemas.create_order_schema import InsideProductsSchema, CreateOrderSchema
from utils.schemas.register_request_schema import RegisterRequestSchema
from utils.validator import Validations
from random import randrange



@pytest.fixture(scope='session')
def api_client():
    return APIClient()

@pytest.fixture
def assertion():
    return Assertions()

@pytest.fixture
def validation():
    return Validations()

@pytest.fixture(scope='session')
def all_products(api_client):

    params = Products(
        category=random.choice(CATEGORIES),
        limit=randrange(1, 10)
    )

    resp = api_client.get_products(
        data=params
    )

    return resp, params


@pytest.fixture(scope='session')
def get_one_product(api_client, all_products):

    resp, params = all_products
    product_id = random.choice(resp.json()['products'])

    resp = api_client.get_single_product(
        product_id=product_id['id']
    )

    return resp, product_id

@pytest.fixture(scope='session')
def email_generator():
    return Generator().client_generator()

@pytest.fixture(scope='session')
def register_module():
    return RegisterModule()

@pytest.fixture(scope='session')
def order_generator():
    return Generator().order_generator()

@pytest.fixture(scope='session')
def token_from_client(api_client, email_generator, register_module):

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

    headers['x-api-key'] = resp.json()['token']

    return headers, resp

@pytest.fixture(scope='session')
def create_order(api_client, token_from_client):

    headers, _ = token_from_client

    num_clients = randrange(1, 5)

    clients_request = []
    clients_response = []
    status_codes = []

    for _ in range(num_clients):
        order_from_customer = Generator().order_generator()

        order_data = {
            'customerName': order_from_customer.customerName,
            'products': [p.__dict__ for p in order_from_customer.products]
        }

        # order_data = OrderBuilder().build()

        final_data = CreateOrderModule().data_molder(
            data=order_data,
            schema=CreateOrderSchema,
            subschema=InsideProductsSchema
        )

        clients_request.append(json.loads(final_data))

        resp = api_client.create_order(
            data=final_data,
            headers=headers
        )

        clients_response.append(resp.json())

        status_codes.append(resp.status_code)
        time.sleep(2)


    clients_response.sort(key=lambda x: x['created'])

    order = [item['customerName'] for item in clients_response]

    clients_request.sort(key=lambda x: order.index(x['customerName']))

    print(clients_request)

    return clients_request, clients_response, status_codes

@pytest.fixture(scope='session')
def get_all_orders(api_client, token_from_client):

    headers, _ = token_from_client

    resp = api_client.get_all_orders(
        headers=headers
    )

    return resp






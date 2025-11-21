
import random
import time
from datetime import datetime
from pydoc_data.topics import topics
from uuid import uuid4

import pytest
from sqlalchemy import text

from data.constants import CATEGORIES
from data.dataclasses.products import Products
from data.generator.builder import OrderBuilder
from data.generator.generator import Generator
from modules.create_order import CreateOrderModule
from modules.register_client import RegisterModule
from utils.api_client import APIClient
from utils.assertions import Assertions
from utils.db import Session
from utils.schemas.create_order_schema import InsideProductsSchema, CreateOrderSchema
from utils.schemas.register_request_schema import RegisterRequestSchema
from utils.tables import Clients, OrderItems, Orders
from utils.validator import Validations
from random import randrange
from utils.db import add_to_db
from kafka import KafkaProducer, KafkaConsumer
import json


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
def token_from_client(api_client, email_generator, register_module, get_db_session, add_data_to_db, kafka_producer):

    email = register_module.prepare_data(
        data=email_generator,
        schema=RegisterRequestSchema
    )

    headers = {
         'Content-Type': 'application/json'
    }

    get_db_session.execute(text('DELETE FROM order_items'))
    get_db_session.execute(text('DELETE FROM orders'))
    get_db_session.execute(text('DELETE FROM clients'))
    get_db_session.commit()

    resp = api_client.register_client(
        data=email,
        headers=headers
    )

    kafka_producer.send(
        'register_clients_at_coffee_shop',
        value=json.loads(email)['email']
    )

    kafka_producer.flush()

    clients_to_db = {
        'email': json.loads(email)['email'],
        'token': resp.json()['token'],
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    item = Clients(**clients_to_db)
    add_data_to_db(get_db_session, item)

    headers['x-api-key'] = resp.json()['token']


    return headers, resp, clients_to_db

@pytest.fixture(scope='session')
def create_order(api_client, token_from_client, add_data_to_db, get_db_session, kafka_producer):

    headers, _, _ = token_from_client

    num_clients = randrange(1, 5)

    clients_request = []
    clients_response = []
    status_codes = []

    get_db_session.execute(text('DELETE FROM order_items'))
    get_db_session.commit()
    get_db_session.execute(text('DELETE FROM orders'))
    get_db_session.commit()


    for i in range(num_clients):
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

        slovar = json.loads(final_data)

        order_id = resp.json()

        customer_name = slovar['customerName']

        name_order_to_db = Orders(
            customer_name=customer_name,
            id=order_id['id'],
            token=headers['x-api-key'],
            clientId=order_id['clientId']
        )

        add_data_to_db(get_db_session, name_order_to_db)

        for i in slovar['products']:
            id = i['id']
            quant = i['quantity']
            make_order_to_db = OrderItems(
            product_id=id,
            quantity=quant,
            order_id=order_id['id'],
            created=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            add_data_to_db(get_db_session, make_order_to_db)

        kafka_producer.send(
            'orders_at_coffee_shop',
            value=resp.json()
        )

        kafka_producer.flush()

        clients_response.append(resp.json())

        status_codes.append(resp.status_code)
        time.sleep(2)


    clients_response.sort(key=lambda x: x['created'])

    order = [item['customerName'] for item in clients_response]

    clients_request.sort(key=lambda x: order.index(x['customerName']))

    return clients_request, clients_response, status_codes

@pytest.fixture(scope='session')
def get_all_orders(api_client, token_from_client):

    headers, _, _ = token_from_client

    resp = api_client.get_all_orders(
        headers=headers
    )

    return resp


@pytest.fixture(scope='session')
def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope='session')
def add_data_to_db():
    return add_to_db


@pytest.fixture(scope='session')
def kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    yield producer
    producer.close()


@pytest.fixture(scope='session')
def kafka_consumer():
    def _create_consumer(topic: str):
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            enable_auto_commit=True
        )
        return consumer
    return _create_consumer








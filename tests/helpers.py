# import requests
#
# from data.constants import PRODUCT_IDS
# from data.dataclasses.products import Products
# from data.endpoints import Endpoints
# from utils.api_client import APIClient
# from conftest import api_client
# from datetime import datetime
# api_client_not_fixture = APIClient()
#
# def get_all_ids(api_client_not_fixture):
#
#     CATEGORIES = ['pastry', 'coffee', 'cookie', 'other']
#
#     PRODUCT_IDS = []
#
#     for item in CATEGORIES:
#         params = Products(
#             category=item
#         )
#
#         resp = api_client_not_fixture.get_products(
#             data=params
#         )
#         products = (resp.json()['products'])
#
#         for product in products:
#             PRODUCT_IDS.append(product['id'])
#
#     with open('C:/Users/user/PycharmProjects/PythonProject9/data/constants.py', 'w', encoding='utf-8') as f:
#         f.write(f'PRODUCT_IDS = {PRODUCT_IDS}\n')
#         f.write(f'CATEGORIES = {CATEGORIES}\n')
#
#     print(f'Записано {len(PRODUCT_IDS)} ID в constants.py')
#
#     return PRODUCT_IDS
#
# get_all_ids(api_client_not_fixture)
from datetime import datetime, timezone, timedelta

# def get_all_descriptions():
#
#     DESCRIPTIONS = []
#
#     for item in PRODUCT_IDS:
#
#         resp = requests.get(
#             url=f'{Endpoints().BASE_URL}{Endpoints().PRODUCTS}/{item}'
#         )
#
#         DESCRIPTIONS.append(resp.json())
#
#
#     with open('C:/Users/user/PycharmProjects/PythonProject9/data/descr.py', 'w', encoding='utf-8') as f:
#         f.write(f'DESCRIPTIONS = {DESCRIPTIONS}\n')
#
#
#     print(f'Записано {len(DESCRIPTIONS)} DESCR в descr.py')
#
#     return DESCRIPTIONS
#
# get_all_descriptions()


#
#
# resp = [('3KMS1E-N7', 'H1K4SiQmu', datetime(2025, 11, 20, 1, 12, 13), 'Christina Stephens', 4006, 4), ('DBC--LAFO', 'DqqSxoQC_', datetime(2025, 11, 20, 1, 0, 44), 'Kenneth Barrett', 2007, 6), ('DBC--LAFO', 'DqqSxoQC_', datetime(2025, 11, 20, 1, 0, 44), 'Kenneth Barrett', 3002, 4), ('FHFU0K-9O', 'actEdqEeg', datetime(2025, 11, 20, 0, 59, 31), 'Timothy Hunt', 4005, 8), ('FHFU0K-9O', 'actEdqEeg', datetime(2025, 11, 20, 0, 59, 31), 'Timothy Hunt', 1003, 5), ('FHFU0K-9O', 'actEdqEeg', datetime(2025, 11, 20, 0, 59, 31), 'Timothy Hunt', 2003, 9), ('KE9G50HVF', 'H1K4SiQmu', datetime(2025, 11, 20, 1, 12, 10), 'Shannon Haley', 4002, 6), ('KE9G50HVF', 'H1K4SiQmu', datetime(2025, 11, 20, 1, 12, 10), 'Shannon Haley', 4004, 8), ('KE9G50HVF', 'H1K4SiQmu', datetime(2025, 11, 20, 1, 12, 10), 'Shannon Haley', 2002, 6), ('KE9G50HVF', 'H1K4SiQmu', datetime(2025, 11, 20, 1, 12, 10), 'Shannon Haley', 1002, 8), ('NVEYMQTCO', 'OjqDV2euP', datetime(2025, 11, 19, 23, 20, 38), 'Steven Berg', 2005, 3)]
def tuple_handler(resp):

    data = []

    for item in resp:

        existing = None
        for x in data:
            if x['customerName'] == item[3]:
                existing = x
                break

        if existing:
            existing['products'].append(
                {
                    'id': item[4],
                    'quantity': item[5]
                }
            )
        else:
            order = {
                'id': item[0],
                'clientId': item[1],
                'created': str(item[2]),
                'customerName': item[3],
                'products': [{
                'id': item[4],
                'quantity': item[5]
                }]
            }

            data.append(order)
    return data
#
# print(tuple_handler(resp))

# resp = [('3KMS1E-N7', datetime(2025, 11, 20, 1, 12, 13), 'Christina Stephens'), ('3KMS1E-N7', datetime(2025, 11, 20, 1, 12, 13), 'Christina Stephens'), ('DBC--LAFO', datetime(2025, 11, 20, 1, 0, 44), 'Kenneth Barrett')]

def tuple_handler2(resp):

    data = []

    for item in resp:

        existing = None
        for x in data:
            if x['customerName'] == item[2]:
                existing = x
                break

        if existing:
            continue
        else:
            order = {
                'id': item[0],
                'customerName': item[2]
            }

            data.append(order)
    return data

# print(tuple_handler2(resp))


# from kafka.admin import KafkaAdminClient, NewTopic
#
# admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092")
#
# topic_list = [NewTopic(name="orders_at_coffee_shop", num_partitions=1, replication_factor=1)]
# admin_client.create_topics(new_topics=topic_list, validate_only=False)
#
# print("Топик создан")


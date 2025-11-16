from data.dataclasses.products import Products
from utils.api_client import APIClient

api_client_not_fixture = APIClient()

def get_all_ids(api_client_not_fixture):

    CATEGORIES = ['pastry', 'coffee', 'cookie', 'other']

    PRODUCT_IDS = []

    for item in CATEGORIES:
        params = Products(
            category=item
        )

        resp = api_client_not_fixture.get_products(
            data=params
        )
        products = (resp.json()['products'])

        for product in products:
            PRODUCT_IDS.append(product['id'])

    with open('C:/Users/user/PycharmProjects/PythonProject9/data/constants.py', 'w', encoding='utf-8') as f:
        f.write(f'PRODUCT_IDS = {PRODUCT_IDS}\n')
        f.write(f'CATEGORIES = {CATEGORIES}\n')

    print(f'Записано {len(PRODUCT_IDS)} ID в constants.py')

    return PRODUCT_IDS

get_all_ids(api_client_not_fixture)
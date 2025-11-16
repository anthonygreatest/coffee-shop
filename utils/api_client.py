import requests

from data.endpoints import Endpoints
from data.endpoints import url_maker

class APIClient:

    def __init__(self):
        self.session = requests.Session()
        self.endpoints = Endpoints()

    def get_status(self):
        return self.session.get(
            url=f'{self.endpoints.BASE_URL}{self.endpoints.STATUS}'
        )

    def get_products(self, data=None):
        return self.session.get(
            url=url_maker(self.endpoints.PRODUCTS, data)
        )

    def get_single_product(self, product_id):
        return self.session.get(
            url=f'{self.endpoints.BASE_URL}{self.endpoints.PRODUCTS}/{product_id}'
        )

    def register_client(self, data, headers):
        return self.session.post(
            url=f'{self.endpoints.BASE_URL}{self.endpoints.CLIENTS}',
            data=data,
            headers=headers
        )

    def create_order(self, data, headers):
        return self.session.post(
            url=f'{self.endpoints.BASE_URL}{self.endpoints.ORDERS}',
            data=data,
            headers=headers
        )

    def get_all_orders(self, headers):
        return self.session.get(
            url=f'{self.endpoints.BASE_URL}{self.endpoints.ORDERS}',
            headers=headers
        )

    def get_order_by_id(self, id, headers):
        return self.session.get(
            url=f'{self.endpoints.BASE_URL}{self.endpoints.ORDERS}/{id}',
            headers=headers
        )
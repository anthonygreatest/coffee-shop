import random
from random import randrange


from faker import Faker

from data.constants import PRODUCT_IDS


faker = Faker()

class OrderBuilder:


    def __init__(self):
        self.result = {
            'customerName': None,
            'products': []
        }

    def populate_your_own(self, product_id, product_quantity):
        self.result['products'].append({
            'id': product_id,
            'quantity': product_quantity
        })
        return self

    def your_name(self, name):
        self.result['customerName'] = name
        return self

    def populate_random(self, num=3):
        for _ in range(num):
            product_id = random.choice(PRODUCT_IDS)
            product_quantity = randrange(1, 5)
            self.result['products'].append({
                'id': product_id,
                'quantity': product_quantity
            })
        return self


    def build(self):
        if self.result['customerName'] is None:
            self.result['customerName'] = faker.name()

        if not self.result['products']:
            self.populate_random()

        return self.result

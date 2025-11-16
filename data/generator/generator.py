
from random import random, randrange
import random

from faker import Faker


from data.constants import PRODUCT_IDS
from data.dataclasses.client import Client
from data.dataclasses.order import Order, ListProducts


class Generator:

    fake = Faker()

    def client_generator(self):

        return Client(
            email=self.fake.email()
        )


    def order_generator(self):
        num_prod = randrange(1, 5)

        products=[ListProducts(id=random.choice(PRODUCT_IDS), quantity=randrange(1, 10))
                      for _ in range(num_prod)]
        return Order(
            customerName=self.fake.name(),
            products=products
        )


# g1 = Generator().order_generator()
#
# data = {
#     'customerName': g1.customerName,
#     'products': [p.__dict__ for p in g1.products]
# }
#
# print(data)

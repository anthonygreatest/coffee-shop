
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

    def generate_long_email(self):

        email_text = (self.fake.text(max_nb_chars=200).replace(' ', '').replace('.', '_').replace('\n', '').rstrip('_')).lower()

        return f'{email_text}@{self.fake.domain_name()}'

    def generate_long_name(self):

        return self.fake.text(max_nb_chars=200).replace(' ', '').replace('.', '_').replace('\n', '').rstrip('_').lower()

# d1 = Generator().generate_long_name()
# print(d1)

# g1 = Generator().order_generator()
#
# data = {
#     'customerName': g1.customerName,
#     'products': [p.__dict__ for p in g1.products]
# }
#
# print(data)

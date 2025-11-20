
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from utils.db import Model


class Clients(Model):
    __tablename__ = 'clients'

    email = Column(String, primary_key=True)
    token = Column(String)
    created_at = Column(String)


class Orders(Model): #родитель, его удаляем, дети удаляются каскадом
    __tablename__ = 'orders'

    id = Column(String, primary_key=True)
    token = Column(String)
    customer_name = Column(String)
    clientId = Column(String)

    items = relationship(
        "OrderItems",
        back_populates="order",
        cascade="all, delete-orphan"
    )

class OrderItems(Model):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"))
    product_id = Column(String)
    quantity = Column(Integer)
    created = Column(String)

    order = relationship("Orders", back_populates="items")
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Enum)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable = False)
    email = Column(String(32), nullable = False, unique = True)
    password = Column(String(256), nullable = False)
    address = Column(String(64))
    create_time = Column(DateTime, default = func.now())
    role = Column(Enum("user", "admin", name="role_enum"), nullable=False, default="user")
    orders = relationship('Order', backref = 'user')

class Medicine(Base):
    __tablename__ = 'medicine'
    id = Column(Integer, primary_key = True)
    name = Column(String(32), nullable = False, unique = True)
    price = Column(Integer, nullable = False)
    quantity = Column(Integer, nullable = False)
    description = Column(String(256))

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key = True)
    create_time = Column(DateTime, default = func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    status = Column(String, nullable=False, default='pending')

class OrderHasMedicine(Base):
    __tablename__ = 'order_has_medicine'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    medicine_id = Column(Integer, ForeignKey('medicine.id'))
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    medicine = relationship(Medicine, backref='order_items')
    order = relationship(Order, backref='order_items')


class MedicineOnDemand(Base):
    __tablename__ = 'medicine_on_demand'
    id = Column(Integer, primary_key = True)
    name = Column(String(32), nullable = False, unique = True)
    quantity = Column(Integer, nullable=False)
    create_time = Column(DateTime, default = func.now())

def update(obj, kwargs: dict):
    kwargs = {k: v for k, v in kwargs.items() if kwargs[k] is not None}
    for key, value in kwargs.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
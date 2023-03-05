from sqlalchemy import (Table, Column, Integer, String, DateTime, ForeignKey, Enum)
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

class OrderHasMedicine(Base):
    __tablename__ = 'order_has_medicine'
    medicine_id = Column(Integer, ForeignKey('medicine.id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    medicine = relationship(Medicine, backref='orders')
    order = relationship(Order, backref='medicine')

    @property
    def name(self):
        return self.medicine.name

class MedicineOnDemand(Base):
    __tablename__ = 'medicine_on_demand'
    id = Column(Integer, primary_key = True)
    name = Column(String(32), nullable = False, unique = True)
    quantity = Column(Integer, nullable=False)
    create_time = Column(DateTime, default = func.now())

def update(obj, kwargs):
    for key, value in kwargs.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
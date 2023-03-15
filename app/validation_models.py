from marshmallow import Schema, fields, post_load, ValidationError, pre_dump
from .models import Medicine, User, Order, OrderHasMedicine, MedicineOnDemand
from .db import session_factory

class MedicineSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Int(required=True)
    quantity = fields.Int(required=True)
    description = fields.Str()

    @post_load
    def deserialize_medicine(self, data, **kwargs):
        return Medicine(**data)

class OrderSchema(Schema):
    create_time = fields.DateTime()
    medicine = fields.Nested(MedicineSchema, many=True, only=("name", "quantity"))

    @post_load
    def deserialize_order(self, data, **kwargs):
        order = Order(medicine = [])
        with session_factory() as session:
            for d in data['medicine']:
                med = session.query(Medicine).filter_by(name = d.name).first()
                print(med)
                if med is None:
                    medicine_on_demand = MedicineOnDemand(name=d.name, quantity=d.quantity)
                    session.add(medicine_on_demand)
                    session.commit()
                    raise ValidationError(f"{d.name} not found")
                elif d.quantity <= 0 or med.quantity < d.quantity:
                    raise ValidationError('Not enough quantity')
                order.medicine.append(OrderHasMedicine(medicine=med, quantity=d.quantity))
        return order

class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    address = fields.Str(required=True)

    @post_load
    def deserealize_user(self, data, **kwargs):
        return User(**data)
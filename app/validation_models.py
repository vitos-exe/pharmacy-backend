from marshmallow import Schema, fields, post_load, ValidationError, pre_dump
from .models import Medicine, User, Order, OrderHasMedicine, MedicineOnDemand
from .db import session_factory

class MedicineSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    price = fields.Int(required=True)
    quantity = fields.Int(required=True)
    description = fields.Str()

    @post_load
    def deserialize_medicine(self, data, **kwargs):
        return Medicine(**data)

class OrderSchema(Schema):
    id = fields.Integer()
    create_time = fields.DateTime()
    order_items= fields.Nested(MedicineSchema, many=True, only=("name", "quantity"))
    status = fields.String()
    
    @post_load
    def deserialize_order(self, data, **kwargs):
        order = Order(order_items = [])
        with session_factory() as session:
            for d in data['order_items']:
                med = session.query(Medicine).filter_by(name = d.name).first()
                print(med)
                if med is None:
                    medicine_on_demand = MedicineOnDemand(name=d.name, quantity=d.quantity)
                    session.add(medicine_on_demand)
                    session.commit()
                    raise ValidationError(f"{d.name} not found")
                elif d.quantity <= 0 or med.quantity < d.quantity:
                    raise ValidationError('Not enough quantity')
                order.order_items.append(OrderHasMedicine(medicine=med, name = d.name,quantity=d.quantity))
        return order


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    address = fields.Str(required=True)
    role = fields.Str()

    @post_load
    def deserealize_user(self, data, **kwargs):
        return User(**data)
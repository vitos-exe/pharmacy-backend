from flask import Blueprint, request, abort, Response
from ..validation_models import OrderSchema
from ..db import session_factory
from ..models import Order
from ..auth import auth
from marshmallow import ValidationError

order = Blueprint('order', __name__, url_prefix = '/order')
order_schema = OrderSchema()

@order.post('/')
@auth.login_required
def create_order():
    try:
        order = order_schema.load(request.get_json())
    except ValidationError as e:
        return e.normalized_messages(), 400
    with session_factory() as session:
        order.user = auth.current_user()
        session.add(order)
        session.commit()
        return order_schema.dump(order)

@order.get('/<int:id>')
@auth.login_required
def get_order(id):
    with session_factory() as session:
        order = session.query(Order).filter_by(id = id).first()
        if order is None:
            return "Not found", 404
        user = auth.current_user()
        if order.user_id != user.id and user.role != "admin":
            return "Access denied", 403
        return order_schema.dump(order)
    
@order.put('/<int:id>')
@auth.login_required(role='admin')
def change_status(id):
    status = request.get_json().get("status")
    if status is None:
        return "Bad request", 400
    
    with session_factory() as session:
        order = session.query(Order).filter_by(id=id).first()
        if order is None:
            return "Not found", 404
        order.status = status
        session.commit()
    return "Success", 200

@order.delete('/<int:id>')
@auth.login_required
def delete_order(id):
    with session_factory() as session:
        order = session.query(Order).filter_by(id = id).first()
        if order is None:
            return "Not found", 404
        user = auth.current_user()
        if order.user_id != user.id and user.role != "admin":
            return "Access denied", 403
        session.delete(order)
        session.commit()
    return 200

@order.get("/my")
@auth.login_required
def get_my_orders():
    user = auth.current_user()
    with session_factory() as session:
        orders = session.query(Order).filter_by(user_id = user.id).all()
        return order_schema.dump(orders, many=True)
    
@order.get("/")
@auth.login_required(role='admin')
def get_all_orders():
    with session_factory() as session:
        orders = session.query(Order).all()
        return order_schema.dump(orders, many=True)
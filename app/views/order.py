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
        order = order_schema.load(request.json)
    except ValidationError as e:
        abort(Response(e.messages_dict['_schema'][0], 400))
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
            abort(Response('Order not found', 404))
        user = auth.current_user()
        if order.user_id != user.id and user.role != "admin":
            abort(Response("Access denied", 403))
        return order_schema.dump(order)

@order.delete('/<int:id>')
@auth.login_required
def delete_order(id):
    with session_factory() as session:
        order = session.query(Order).filter_by(id = id).first()
        if order is None:
            abort(Response('Order not found', 404))
        user = auth.current_user()
        if order.user_id != user.id and user.role != "admin":
            abort(Response("Access denied", 403))
        session.delete(order)
        session.commit()
    return 200

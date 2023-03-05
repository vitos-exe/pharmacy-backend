from werkzeug.security import generate_password_hash
from flask import Blueprint, request, Response, abort
from ..models import User, update
from ..db import session_factory
from ..validation_models import UserSchema
from ..auth import return_auth

auth = return_auth()

user = Blueprint('user', __name__, url_prefix = '/user')
user_schema = UserSchema()

@user.post('/')
def create_user():
    try:
        user = UserSchema().load(request.get_json())
    except:
        abort(Response('Validation failed', 400))
    user.password = generate_password_hash(user.password)
    with session_factory() as session:
        if session.query(User).filter_by(email = user.email).first() is not None:
            abort(Response('User with such email already exists', 400))
        session.add(user)
        session.commit()
        return user_schema.dump(user), 201

@user.get('/<int:id>')
@auth.login_required
def get_user(id):
    with session_factory() as session:
        user = session.query(User).filter_by(id = id).first()
    if user is None:
        abort(Response('User not found', 404))
    current_user = auth.current_user()
    if current_user.id != user.id and current_user.role != "admin":
        abort(Response("Access denied", 403))
    return user_schema.dump(user), 200

@user.put('/<int:id>')
@auth.login_required
def update_user(id):
    try:
        updated = user_schema.load(request.get_json())
    except:
        abort(Response('Validation failed', 400))
    updated.password = generate_password_hash(updated.password)
    with session_factory() as session:
        user = session.query(User).filter_by(id = id).first()
        if user is None:
            abort(Response('User not found', 404))
        current_user = auth.current_user()
        if (current_user.user_id != user.id and current_user.role != "admin") or \
                (updated.role == 'admin' and current_user.role != 'admin'):
            abort(Response("Access denied", 403))
        try:
            update(user, UserSchema().dump(updated))
            session.commit()
        except:
            abort(Response('Validation failed', 400))
    return user_schema.dump(user), 200

@user.delete('/<int:id>')
@auth.login_required
def delete_user(id):
    with session_factory() as session:
        user = session.query(User).filter_by(id = id).first()
        if user is None:
            abort(Response('User not found', 404))
        current_user = auth.current_user()
        if current_user.user_id != user.id and current_user.role != "admin":
            abort(Response("Access denied", 403))
        session.delete(user)
        session.commit()
    return 200
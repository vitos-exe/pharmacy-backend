from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, Response, abort
from ..models import User, update
from ..db import session_factory
from ..validation_models import UserSchema
from ..auth import auth
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError


user = Blueprint('user', __name__, url_prefix = '/user')
user_schema = UserSchema()

@user.get("/")
@auth.login_required(role='admin')
def get_all_users():
    with session_factory() as session:
        return UserSchema(partial=['password']).dump(session.query(User).all(), many=True);

@user.post('/')
def create_user():
    try:
        user = UserSchema().load(request.get_json())
    except ValidationError as e:
        return e.normalized_messages(), 400 
    user.password = generate_password_hash(user.password)
    with session_factory() as session:
        if session.query(User).filter_by(email = user.email).first() is not None:
            return 'User with such email already exists', 400
        session.add(user)
        session.commit()
        return user_schema.dump(user), 201
@user.get('/me')
@auth.login_required
def get_me():
    return UserSchema(partial=["password"]).dump(auth.current_user())

@user.put('/<int:id>')
@auth.login_required
def update_user(id):
    try:
        updated = UserSchema(partial=True).load(request.get_json())
    except ValidationError as e:
        return e.normalized_messages(), 400
    with session_factory() as session:
        user = session.query(User).filter_by(id = id).first()
        if user is None:
            return 'Not found', 404
        current_user = auth.current_user()
        if (current_user.id != user.id and current_user.role != "admin") or \
                (updated.role == 'admin' and current_user.role != 'admin'):
            return "Access denied", 403
        try:
            if updated.password is not None:
                updated.password = generate_password_hash(updated.password)

            update(user, UserSchema().dump(updated))
            session.commit()
            users = session.query(User).all()[1]
            return UserSchema(only=['email', 'address', 'email', 'name', 'id']).dump(user), 200
        except IntegrityError:
            return 'Validation failed', 400

@user.delete('/<int:id>')
@auth.login_required
def delete_user(id):
    with session_factory() as session:
        user = session.query(User).filter_by(id = id).first()
        if user is None:
            return 'Not found', 404
        current_user = auth.current_user()
        if current_user.id != user.id and current_user.role != "admin":
            return "Access denied", 403
        session.delete(user)
        session.commit()
    return "Success", 200
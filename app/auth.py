from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from .db import session_factory
from .models import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    with session_factory() as session:
        user = session.query(User).filter_by(email=username).first()
        if user is not None and check_password_hash(user.password, password):
            return user
        
@auth.get_user_roles
def get_roles(user):
    return user.role
from .models import User, Medicine, Order, OrderHasMedicine
from werkzeug.security import generate_password_hash

_user = User(
        name = "Vitaliy",
        email = "vivich4omega@gmail.com",
        password = generate_password_hash("oken"),
        role = "user",
        address = "Lviv"
    )

_admin = User(
    name = "Anton",
    email = "admin@gmail.com",
    password = generate_password_hash("oken"),
    role = "admin",
    address = "Rotterdam"
)

_ibuprofen = Medicine(
    name = "Ibuprofen",
    price = 50,
    quantity = 25
)

_nurofen = Medicine(
    name = "Nurofen",
    price = 10,
    quantity = 30
)

_order = Order(
    user=_user,
    medicine=[
        OrderHasMedicine(
            medicine=_ibuprofen,
            quantity=10
        ),
        OrderHasMedicine(
            medicine=_nurofen,
            quantity=15
        )
    ]
)

test_data = [_user, _admin, _ibuprofen, _nurofen, _order]
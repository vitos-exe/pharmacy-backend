from .models import User, Medicine, Order, OrderHasMedicine, MedicineOnDemand
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
    quantity = 25,
    description = "Desciption"
)

_nurofen = Medicine(
    name = "Nurofen",
    price = 10,
    quantity = 30,
    description = "Desciption"
)

_order = Order(
    user=_user,
    order_items=[
        OrderHasMedicine(
            name=_ibuprofen.name,
            medicine=_ibuprofen,
            quantity=10
        ),
        OrderHasMedicine(
            name=_nurofen.name,
            medicine=_nurofen,
            quantity=15
        )
    ]
)

_medicine_on_demand_1 = MedicineOnDemand(
    name='Unknown name',
    quantity=10
)

test_data = [_user, _admin, _ibuprofen, _nurofen, _order, _medicine_on_demand_1]
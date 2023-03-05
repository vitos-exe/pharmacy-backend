from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base
from werkzeug.security import generate_password_hash
from .models import User, Medicine, Order, OrderHasMedicine

engine = create_engine('postgresql+pg8000://postgres:@localhost/pharmacy')

session_factory = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind = engine
))

def recreate_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def init_instances():
    user = User(
        name = "Vitaliy",
        email = "vivich4omega@gmail.com",
        password = generate_password_hash("oken"),
        role = "user",
        address = "Lviv"
    )

    admin = User(
        name = "Anton",
        email = "admin@gmail.com",
        password = generate_password_hash("oken"),
        role = "admin",
        address = "Rotterdam"
    )

    medicine1 = Medicine(
        name = "Ibuprofen",
        price = 50,
        quantity = 25
    )

    medicine2 = Medicine(
        name = "Nurofen",
        price = 10,
        quantity = 30
    )

    order = Order(user=user)

    order_medicine1 = OrderHasMedicine(
        order=order,
        medicine=medicine1,
        quantity=10
    )

    order_medicine2 = OrderHasMedicine(
        order=order,
        medicine=medicine2,
        quantity=15
    )

    with session_factory() as session:
        session.add_all([user, admin, medicine1, medicine2, order, order_medicine1, order_medicine2])
        session.commit()

def create_db_cli_commands(app):
    @app.cli.command("init-db")
    def init_db_command():
        recreate_tables()
        print("DB reinitialized")

    @app.cli.command("init-instances")
    def init_instances_command():
        init_instances()
        print("Instances initialized")
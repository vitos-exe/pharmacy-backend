from flask import Blueprint, request, abort, Response
from ..models import Medicine, update, MedicineOnDemand
from ..db import session_factory
from ..validation_models import MedicineSchema
from ..auth import auth
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound

medicine = Blueprint('medicine', __name__, url_prefix = '/medicine')
medicine_schema = MedicineSchema()
medicine_on_demand_schema = MedicineSchema(only=('name', 'quantity'))

@medicine.post("/")
@auth.login_required(role='admin')
def create_medicine():
    try:
        medicine = medicine_schema.load(request.json)
    except ValidationError as e:
        return e.normalized_messages(), 400
    with session_factory() as session:
        try:
            session.add(medicine)
            session.commit()
            new = medicine_schema.dump(medicine)
            remove_medicine_from_demand(medicine.name, medicine.quantity)
            return new, 201
        except IntegrityError:
            return {"name": 'Medicine with the same name already exists'}, 400
    
    
@medicine.get('/')
def get_all_medicine():
    with session_factory() as session:
        medicine = session.query(Medicine).all()
        if len(medicine) ==  0:
            return {"name":  "No entitires found"}, 404 

        return medicine_schema.dump(medicine, many=True)

@medicine.get('/demand')
@auth.login_required(role='admin')
def get_medicine_on_demand():
    with session_factory() as session:
        medicine_on_demand = session.query(MedicineOnDemand).all()

        return medicine_on_demand_schema.dump(medicine_on_demand, many=True)
    
@medicine.post('/demand')
@auth.login_required
def add_medicine_on_demand():
    try:
        medicine_on_demand = medicine_on_demand_schema.load(request.json)
    except ValidationError as e:
        return e.normalized_messages(), 400
    
    with session_factory() as session:
        try:
            session.add(medicine_on_demand)
        except IntegrityError:
            existed = session.query(MedicineOnDemand).filter_by(name=medicine_on_demand.name).first()
            existed.quantity += medicine_on_demand.quantity
        session.commit()
        return medicine_on_demand_schema.dump(medicine_on_demand), 201

@medicine.get('/<int:id>')
def get_medicine(id):
    with session_factory() as session:
        try:
            medicine = session.query(Medicine).filter_by(id = id).one()
        except NoResultFound:
            return {"name": "Not found"}, 404
        return medicine_schema.dump(medicine), 200

@medicine.put('/<int:id>')
@auth.login_required(role='admin')
def update_medicine(id):
    try:
        updated = MedicineSchema(partial=True).load(request.get_json())
    except ValidationError as e:
        return e.normalized_messages(), 400
    with session_factory() as session:
        try:
            medicine = session.query(Medicine).filter_by(id = id).one()
        except NoResultFound:
            return {'name': 'Not found'}, 404
        
        try:
            update(medicine, medicine_schema.dump(updated))
            session.commit()
        except IntegrityError:
            return {'name': 'Medicine with the same name already exists'}, 400
        
        return medicine_schema.dump(medicine), 200

@medicine.delete('/<int:id>')
@auth.login_required(role='admin')
def delete_medicine(id):
    with session_factory() as session:
        try:
            medicine = session.query(Medicine).filter_by(id = id).one()
        except NoResultFound:
            return {'name': 'Not found'}, 404
        session.delete(medicine)
        session.commit()
        return "Success", 200

def remove_medicine_from_demand(name: str, quantity: int) -> None:
    with session_factory() as session:
        medicine_on_demand = session.query(MedicineOnDemand).filter_by(name=name).first()
        if medicine_on_demand is not None:
            if quantity >= medicine_on_demand.quantity:
                session.delete(medicine_on_demand)
            else:
                medicine_on_demand.quantity -= quantity
        session.commit()
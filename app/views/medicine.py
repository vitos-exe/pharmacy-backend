from flask import Blueprint, request, abort, Response
from ..models import Medicine, update, MedicineOnDemand
from ..db import session_factory
from ..validation_models import MedicineSchema
from ..auth import auth

medicine = Blueprint('medicine', __name__, url_prefix = '/medicine')
medicine_schema = MedicineSchema()

@medicine.post("/")
@auth.login_required(role='admin')
def create_medicine():
    try:
        medicine = medicine_schema.load(request.get_json())
    except:
        abort(Response('Validation failed', 400))
    with session_factory() as session:
        if session.query(Medicine).filter_by(name = medicine.name).first() is not None:
            abort(Response('Medicine with the same name already exists', 400))
        session.add(medicine)
        session.commit()
        return medicine_schema.dump(medicine), 201
    
@medicine.get('/')
def get_all_medicine():
    with session_factory() as session:
        medicine = session.query(Medicine).all()
        return medicine_schema.dump(medicine, many=True)

@medicine.get('/demand')
@auth.login_required(role='admin')
def get_medicine_on_demand():
    with session_factory() as session:
        medicine_on_demand = session.query(MedicineOnDemand).all()
        return MedicineSchema(only=('name', 'quantity')).dump(medicine_on_demand, many=True)
    
@medicine.delete('/demand/<int:id>')
@auth.login_required(role='admin')
def delete_medicine_on_demand(id):
    with session_factory() as session:
        medicine_on_demand = session.query(MedicineOnDemand).filter_by(id=id).first()
        if medicine_on_demand is None:
            abort(Response('Medicine not found', 404))
        session.delete(medicine_on_demand)
        session.commit()
    return 200

@medicine.get('/<int:id>')
def get_medicine(id):
    with session_factory() as session:
        medicine = session.query(Medicine).filter_by(id = id).first()
    if medicine is None:
        abort(Response('Medicine not found', 404))
    return medicine_schema.dumps(medicine), 200

@medicine.put('/<int:id>')
@auth.login_required(role='admin')
def update_medicine(id):
    try:
        updated = medicine_schema.load(request.get_json())
    except:
        abort(Response('Validation failed', 400))
    with session_factory() as session:
        medicine = session.query(Medicine).filter_by(id = id).first()
        if medicine is None:
            abort(Response('Medicine not found', 404))
        try:
            update(medicine, medicine_schema.dump(updated))
            session.commit()
        except:
            abort(Response('Validation failed', 400))
        return medicine_schema.dump(medicine), 200

@medicine.delete('/<int:id>')
@auth.login_required(role='admin')
def delete_medicine(id):
    with session_factory() as session:
        medicine = session.query(Medicine).filter_by(id = id).first()
        if medicine is None:
            abort(Response('Medicine not found', 404))
        session.delete(medicine)
        session.commit()
    return 200

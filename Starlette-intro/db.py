# file name is arbitrary
from database import Session, engine
from models import Student

local_session=Session(bind=engine)

def get_all_students():
    return local_session.query(Student).all()
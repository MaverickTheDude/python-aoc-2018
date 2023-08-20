# usage:  python create_db.py
from database import Base,engine
from models import Student

Base.metadata.create_all(bind=engine)


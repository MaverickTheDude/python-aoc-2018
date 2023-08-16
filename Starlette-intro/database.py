from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


BASE_DIR=os.path.dirname(os.path.relpath(__file__))

print("file: " + os.path.relpath(__file__))
print("Base Dir: " + BASE_DIR)

conn_str="sqlite:///" + os.path.join(BASE_DIR,"students.db")

Base=declarative_base()

Session=sessionmaker()

engine=create_engine(conn_str, echo=True)

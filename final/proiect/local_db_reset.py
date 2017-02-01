from local_db_init import Base
from local_db_stuff import DBStuff
from sqlalchemy import create_engine
import os
import sys

from local_db_init import engine

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

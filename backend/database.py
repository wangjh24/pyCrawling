from sqlalchemy import create_engine
import os
DATABASE_URL = "postgresql://test:1234@db:5432/PyCrawling"
engine = create_engine(DATABASE_URL)
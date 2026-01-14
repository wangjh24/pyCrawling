from sqlalchemy import create_engine

DATABASE_URL = "postgresql://test:1234@localhost:5432/PyCrawling"
engine = create_engine(DATABASE_URL)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    "postgresql://postgres:taran1234@localhost:5432/echodesk",
    echo=True,
)

Base = declarative_base()
Session = sessionmaker(bind=engine)

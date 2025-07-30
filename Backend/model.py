from database import Base
from sqlalchemy import Column, Boolean, Text, Integer, String, ForeignKey
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(50), unique=True)
    password = Column(Text, nullable=False)

    def __repr__(self):
        return f"<User : {self.username}>"


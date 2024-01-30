from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, Session
from .dependencies import get_db_engine
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False)


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

engine = get_db_engine()

# Base.metadata.create_all(engine)

mock_users_db = [
    {
        "id" : 1, 
        "username" : "John_Doe",
        "password" : pwd_context.hash("password1"),
        "verified" : True,
        "disabled" : False
    }

    ,

    {
        "id" : 2, 
        "username" : "Jane_Doe",
        "password" : pwd_context.hash("password2"),
        "verified" : True,
        "disabled" : False
    }
]

# with Session(engine) as session:
#     try :
#         for user in mock_users_db:
#             session.add(User(**user))
#     except Exception as e:
#         print(e)
#     session.commit()
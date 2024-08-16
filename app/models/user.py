from pyodmongo import DbModel, Field
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from typing import ClassVar


class User(DbModel):
    email: str = Field(index=True, unique=True)
    password: str
    _collection: ClassVar = "users"

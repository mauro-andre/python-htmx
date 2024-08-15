from pyodmongo import DbModel
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from typing import ClassVar


class User(DbModel):
    email: str
    password: str
    _collection: ClassVar = "users"

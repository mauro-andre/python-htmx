from pyodmongo import DbModel, Field
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from typing import ClassVar
from datetime import datetime


class Task(DbModel):
    description: str
    deadline: datetime
    _collection: ClassVar = "tasks"

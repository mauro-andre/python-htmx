from pyodmongo import DbModel, Field, Id
from pydantic import ConfigDict
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from typing import ClassVar
from datetime import datetime
from app.models.user import User


class Task(DbModel):
    description: str
    deadline: datetime
    is_done: bool
    user: User | Id
    model_config = ConfigDict(extra="allow")
    _collection: ClassVar = "tasks"

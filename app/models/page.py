from pydantic import BaseModel


class Page(BaseModel):
    title: str
    path: str
    html: str

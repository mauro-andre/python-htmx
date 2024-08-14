from pydantic import BaseModel

class Page(BaseModel):
    title: str
    path: str
    html_core: str
    html_main: str
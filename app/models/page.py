from pydantic import BaseModel
from pyodmongo.queries import sort
from app.db.engine import engine, tz_info
from datetime import datetime
from app.models.task import Task


class Page(BaseModel):
    title: str
    path: str
    html: str

    async def resolve_page(self, access_token: str): ...


class Home(Page):
    on_time: int = 0
    for_today: int = 0
    overdue: int = 0
    tasks: list = []

    async def resolve_page(self, access_token: str):
        self.on_time = 0
        self.for_today = 0
        self.overdue = 0

        query = Task.user == access_token
        sort_tasks = sort((Task.is_done, 1), (Task.deadline, 1))
        self.tasks: list[Task] = await engine.find_many(
            Model=Task, query=query, sort=sort_tasks
        )
        today = datetime.now(tz=tz_info).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        for task in self.tasks:
            if not task.is_done:
                task.status_icon = "fa-envelope-circle-check"
                if today < task.deadline:
                    self.on_time += 1
                    task.status = "A vencer"
                    task.status_class = "success"
                elif today == task.deadline:
                    self.for_today += 1
                    task.status = "Vence hoje"
                    task.status_class = "warning"
                else:
                    self.overdue += 1
                    task.status = "Vencido"
                    task.status_class = "danger"
            else:
                task.status_icon = "fa-envelope-open"
                task.status = "Concluído"
                task.status_class = ""

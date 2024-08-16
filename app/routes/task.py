from fastapi import APIRouter, Form, status, Request, Depends
from fastapi.responses import HTMLResponse
from app.models.user import User
from app.db.engine import engine
from app.routes.credentials_pages import template
from app.models.task import Task
from app.db.engine import tz_info
from datetime import datetime
from app.services.token import verify_token
from app.models.page import Home

router = APIRouter()


@router.post("/")
async def create_task(
    request: Request,
    description: str = Form(...),
    deadline: str = Form(...),
    access_token=Depends(verify_token),
):
    deadline = datetime.fromisoformat(deadline).replace(tzinfo=tz_info)
    new_task = Task(
        description=description, deadline=deadline, is_done=False, user=access_token
    )
    await engine.save(new_task)
    page = Home(title="Home", path="/", html="pages/home.html")
    await page.resolve_page(access_token=access_token)
    return template.TemplateResponse(
        request=request, name=page.html, context={"page": page}
    )


@router.delete("/{task_id}")
async def delete_task(request: Request, task_id, access_token=Depends(verify_token)):
    await engine.delete(Model=Task, query=Task.id == task_id)
    page = Home(title="Home", path="/", html="pages/home.html")
    await page.resolve_page(access_token=access_token)
    return template.TemplateResponse(
        request=request, name=page.html, context={"page": page}
    )


@router.put("/{task_id}")
async def update_task(request: Request, task_id, access_token=Depends(verify_token)):
    task_to_update: Task = await engine.find_one(Model=Task, query=Task.id == task_id)
    task_to_update.is_done = not task_to_update.is_done
    await engine.save(task_to_update)
    page = Home(title="Home", path="/", html="pages/home.html")
    await page.resolve_page(access_token=access_token)
    return template.TemplateResponse(
        request=request, name=page.html, context={"page": page}
    )

from fastapi import APIRouter, Form, HTTPException, status, Request
from app.models.user import User
from app.db.engine import engine
from app.routes.credentials_pages import template

router = APIRouter()


@router.post("/")
async def register_user(
    request: Request, email: str = Form(...), password: str = Form(...)
):
    query = User.email == email
    user_found: User = await engine.find_one(Model=User, query=query)
    html = "partials/alert.html"
    if user_found:
        return template.TemplateResponse(
            request=request,
            name=html,
            context={"alert_class": "alert-danger", "msg": "Usuário já cadastrado"},
            status_code=status.HTTP_400_BAD_REQUEST,
            headers={"X-Should-Swap": "true"},
        )
    new_user = User(email=email, password=password)
    await engine.save(new_user)
    return template.TemplateResponse(
        request=request,
        name=html,
        context={
            "alert_class": "alert-success",
            "msg": "Usuário cadastrado com sucesso",
        },
    )

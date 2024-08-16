from fastapi import APIRouter, Form, status, Request
from fastapi.responses import HTMLResponse
from app.models.user import User
from app.db.engine import engine
from app.routes.credentials_pages import template

router = APIRouter()


@router.post("/register")
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


@router.post("/token")
async def token(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    query = User.email == email
    user_found: User = await engine.find_one(Model=User, query=query)
    html = "partials/alert.html"
    if not user_found or user_found.password != password:
        return template.TemplateResponse(
            request=request,
            name=html,
            context={
                "alert_class": "alert-danger",
                "msg": "Usuário ou senha inválidos",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
            headers={"X-Should-Swap": "true"},
        )
    response = HTMLResponse(content="", headers={"HX-Redirect": "/"})
    response.set_cookie(key="accessToken", value=user_found.id)
    return response


@router.get("/logout")
async def logout(request: Request):
    response = HTMLResponse(content="", headers={"HX-Redirect": "/"})
    response.delete_cookie(key="accessToken")
    return response

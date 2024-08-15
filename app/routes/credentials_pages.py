from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.page import Page

router = APIRouter()

template = Jinja2Templates(directory="app/client")


pages = [
    Page(
        title="Login",
        path="/login",
        html="credentials-pages/login.html",
    ),
    Page(
        title="Cadastro",
        path="/cadastro",
        html="credentials-pages/register.html",
    ),
]


def generate_credentials_routes(page: Page):
    @router.get(page.path, response_class=HTMLResponse)
    async def route(request: Request):
        hx_boosted = request.headers.get("hx-boosted")
        html = page.html if hx_boosted else "credentials-pages/main.html"
        return template.TemplateResponse(
            request=request,
            name=html,
            context={"page": page},
            headers={"X-Page-Title": page.title},
        )


for page in pages:
    generate_credentials_routes(page=page)

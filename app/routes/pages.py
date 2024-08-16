from fastapi import Request, APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.models.page import Page, Home
from app.services.token import verify_token

router = APIRouter()

template = Jinja2Templates(directory="app/client")


pages = [
    Home(
        title="Home",
        path="/",
        html="pages/home.html",
    )
]


def generate_credentials_routes(page: Page):
    @router.get(page.path, response_class=HTMLResponse)
    async def route(request: Request, access_token: str = Depends(verify_token)):
        hx_request = request.headers.get("hx-request")

        if not access_token:
            return RedirectResponse(url="/login")
        await page.resolve_page(access_token=access_token)
        html = page.html if hx_request else "pages/main.html"
        return template.TemplateResponse(
            request=request,
            name=html,
            context={"page": page},
            headers={"X-Page-Title": page.title},
        )


for page in pages:
    generate_credentials_routes(page=page)

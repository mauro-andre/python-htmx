from fastapi import Request, APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.models.page import Page

router = APIRouter()

template = Jinja2Templates(directory="app/client")


pages = [
    Page(
        title="Home",
        path="/",
        html="pages/home.html",
    )
]


async def verify_token(request: Request):
    return request.cookies.get("accessToken")


def generate_credentials_routes(page: Page):
    @router.get(page.path, response_class=HTMLResponse)
    async def route(request: Request, access_token: str = Depends(verify_token)):
        hx_boosted = request.headers.get("hx-boosted")

        if not access_token:
            if not hx_boosted:
                return RedirectResponse(url="/login")
            return HTMLResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"HX-Redirect": "/login"},
            )

        html = page.html if hx_boosted else "pages/main.html"
        return template.TemplateResponse(
            request=request,
            name=html,
            context={"page": page},
            headers={"X-Page-Title": page.title},
        )


for page in pages:
    generate_credentials_routes(page=page)

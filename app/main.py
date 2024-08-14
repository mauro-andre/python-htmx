from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.page import Page

app = FastAPI()

template = Jinja2Templates(directory="app/client")


def response_selector(
    request: Request,
    json_response: JSONResponse,
    html_response: HTMLResponse,
    page: Page,
):
    if request.headers.get("accept") != "application/json":
        hx_boosted = request.headers.get("hx-boosted")
        html_file = page.html_core if hx_boosted else page.html_main
        return html_response
    else:
        return json_response


@app.get("/login")
async def login(request: Request):
    html_response = template.TemplateResponse(
        request=request, name="credentials-pages/login.html"
    )
    json_response = {"Shunda": "Bacana"}
    return response_selector(
        request=request, json_response=json_response, html_response=html_response
    )

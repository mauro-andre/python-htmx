from fastapi import Request, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse


async def verify_token(request: Request):
    hx_request = request.headers.get("hx-request")
    access_token = request.cookies.get("accessToken")

    if not access_token:
        if hx_request:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"HX-Redirect": "/login"},
            )
    return access_token


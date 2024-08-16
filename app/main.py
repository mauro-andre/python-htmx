from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.credentials_pages import router as credentials_pages_router
from app.routes.pages import router as pages_router
from app.routes.users import router as users_router
from app.routes.task import router as task_router


app = FastAPI()

assets = StaticFiles(directory="app/client/assets")
app.mount("/assets", assets, name="assets")

app.include_router(router=credentials_pages_router)
app.include_router(router=pages_router)
app.include_router(router=users_router, prefix="/user")
app.include_router(router=task_router, prefix="/task")

from fastapi import FastAPI
from database import create_tables
from router import config_router, view_config_router, view_forms_router
from fastui import prebuilt_html
from starlette.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

create_tables()
print("База готова к работе")

app = FastAPI()

app.title = "CONFIG KEEPER"

# app.mount("/templates", StaticFiles(directory="templates"), name="templates")
# templates = Jinja2Templates(directory="templates")

# добавление роутеров
app.include_router(config_router)
app.include_router(view_config_router)
app.include_router(view_forms_router)
@app.get("/fastui/{path:path}")
def view_config() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='Конфигурации'))

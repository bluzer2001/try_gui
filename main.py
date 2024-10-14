from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import time

app = FastAPI()

# Указываем путь к шаблонам
templates = Jinja2Templates(directory="templates")

# Главная страница с выбором отчета
@app.get("/")
async def get_report_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Эндпоинт для загрузки отчета
@app.post("/generate_report")
async def generate_report(report_type: str):
    time.sleep(3)  # Имитация задержки для загрузки отчета
    # В реальном случае здесь будет логика обработки данных и генерации отчета
    return JSONResponse({"status": "success", "message": f"Отчет {report_type} сгенерирован!"})

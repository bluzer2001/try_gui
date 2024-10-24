Да, это возможно! Вы можете реализовать функционал, при котором фронтенд (JavaScript) отправляет запрос на сервер (FastAPI) при выборе отчета, и сервер возвращает HTML, который будет динамически добавлен на страницу. Это можно сделать через AJAX-запросы (например, с использованием `fetch`) для получения HTML от бэкенда и последующей вставки этого HTML на страницу.

### Как это сделать:

1. **На стороне клиента (JavaScript)**: При выборе отчета отправить запрос на сервер для получения HTML-элемента с полями для ввода.
2. **На стороне сервера (FastAPI)**: Создать эндпоинт, который будет возвращать HTML-код, зависящий от выбранного отчета.
3. **Динамическая вставка HTML**: Когда клиент получает HTML от сервера, он динамически вставляет его на страницу.

### Шаг 1: Обновление JavaScript на фронтенде

В `static/js/script.js` нужно изменить логику таким образом, чтобы при выборе отчета отправлялся запрос на сервер, и после получения ответа HTML-код добавлялся на страницу.

```javascript
document.addEventListener("DOMContentLoaded", function () {
    const reportDropdown = document.getElementById("report-dropdown");
    const reportParametersContainer = document.getElementById("report-parameters-container");

    // Когда выбран отчет, отправляем запрос на сервер для получения параметров
    reportDropdown.addEventListener("change", function () {
        const selectedReport = reportDropdown.value;

        // Отправляем запрос на сервер для получения HTML параметров
        fetch(`/get_report_parameters/${selectedReport}`)
            .then(response => response.text())
            .then(html => {
                // Вставляем полученный HTML в контейнер для параметров отчета
                reportParametersContainer.innerHTML = html;
            })
            .catch(error => {
                console.error("Ошибка загрузки параметров:", error);
            });
    });
});
```

### Шаг 2: Обновление HTML-шаблона

В `index.html` добавим контейнер, в который будет динамически вставляться HTML с параметрами отчета.

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Сервис отчетов</title>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <h1>Сервис отчетов</h1>

    <!-- Выпадающий список для выбора отчета -->
    <div class="dropdown-container">
        <select id="report-dropdown">
            <option value="" disabled selected>Выберите отчет</option>
            <option value="financial_report">Отчет 1: Финансовый</option>
            <option value="security_report">Отчет 2: Риски безопасности</option>
            <option value="performance_report">Отчет 3: Производительность</option>
        </select>
    </div>

    <!-- Контейнер для параметров отчета, который будет заполняться динамически -->
    <div id="report-parameters-container"></div>

    <!-- Кнопка для генерации отчета -->
    <div class="button-container">
        <button id="generate-report-button" disabled>Показать отчет</button>
    </div>

    <div id="loading-indicator" class="hidden">Загрузка...</div>
    <div id="report-output"></div>

    <script src="/static/js/script.js"></script>
</body>
</html>
```

### Шаг 3: Создание эндпоинта в FastAPI

Теперь добавим эндпоинт на стороне FastAPI, который будет возвращать HTML в зависимости от выбранного отчета.

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Указываем путь к шаблонам
templates = Jinja2Templates(directory="templates")

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def get_report_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Эндпоинт для получения параметров отчета в виде HTML
@app.get("/get_report_parameters/{report_type}", response_class=HTMLResponse)
async def get_report_parameters(report_type: str, request: Request):
    # Здесь можно добавлять разные формы параметров в зависимости от типа отчета
    if report_type == "financial_report":
        return templates.TemplateResponse("financial_report_parameters.html", {"request": request})
    elif report_type == "security_report":
        return templates.TemplateResponse("security_report_parameters.html", {"request": request})
    elif report_type == "performance_report":
        return templates.TemplateResponse("performance_report_parameters.html", {"request": request})
    else:
        return HTMLResponse("<p>Параметры для данного отчета не найдены.</p>")
```

### Шаг 4: Создание HTML-шаблонов для параметров отчета

Теперь создадим отдельные шаблоны для каждого типа отчета в папке `templates`:

#### `financial_report_parameters.html` (пример для финансового отчета)

```html
<div id="report-parameters">
    <h3>Параметры для финансового отчета</h3>
    <div>
        <label for="report-date">Отчетная дата:</label>
        <input type="date" id="report-date">
    </div>
    <div>
        <label for="email">Электронная почта:</label>
        <input type="email" id="email" placeholder="Введите вашу почту">
    </div>
</div>
```

#### `security_report_parameters.html` (пример для отчета по безопасности)

```html
<div id="report-parameters">
    <h3>Параметры для отчета по рискам безопасности</h3>
    <div>
        <label for="security-level">Уровень безопасности:</label>
        <input type="text" id="security-level" placeholder="Введите уровень безопасности">
    </div>
    <div>
        <label for="email">Электронная почта:</label>
        <input type="email" id="email" placeholder="Введите вашу почту">
    </div>
</div>
```

#### `performance_report_parameters.html` (пример для отчета по производительности)

```html
<div id="report-parameters">
    <h3>Параметры для отчета по производительности</h3>
    <div>
        <label for="performance-metric">Показатель производительности:</label>
        <input type="text" id="performance-metric" placeholder="Введите показатель">
    </div>
    <div>
        <label for="email">Электронная почта:</label>
        <input type="email" id="email" placeholder="Введите вашу почту">
    </div>
</div>
```

### Шаг 5: Запуск приложения

После внесения всех изменений перезапустите FastAPI сервер:

```bash
uvicorn main:app --reload
```

### Пояснение:

- **JavaScript** отправляет запрос на сервер, когда пользователь выбирает тип отчета, и получает HTML-код с параметрами.
- **FastAPI** возвращает HTML-код через Jinja2-шаблоны, зависящий от выбранного отчета.
- HTML динамически вставляется на страницу в контейнере `report-parameters-container`.

Теперь, при выборе типа отчета, браузер будет отправлять запрос на сервер, который вернет HTML с полями для ввода параметров отчета, а затем этот HTML будет динамически добавлен на страницу.

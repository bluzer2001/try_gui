Для реализации этой логики добавим на клиенте отправку POST-запроса на сервер после проверки корректности введенных данных. На стороне сервера FastAPI создадим обработчик, который будет проверять параметры, и в зависимости от их корректности возвращать соответствующий статус и сообщение.

### Шаг 1: JavaScript для отправки запроса на сервер и обработки ответа

В `static/js/script.js` обновим код, добавив отправку POST-запроса и обработку ответов от сервера.

```javascript
document.addEventListener("DOMContentLoaded", function () {
    const reportDropdown = document.getElementById("report-dropdown");
    const reportParametersContainer = document.getElementById("report-parameters-container");
    const generateButton = document.getElementById("generate-report-button");
    const errorMessage = document.getElementById("error-message");

    function isValidEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }

    function isValidDate(date) {
        return date !== "";
    }

    function updateButtonState() {
        const reportDate = document.getElementById("report-date")?.value || "";
        const email = document.getElementById("email")?.value || "";

        if (isValidEmail(email) && isValidDate(reportDate)) {
            generateButton.classList.add("active");
            generateButton.classList.remove("inactive");
            generateButton.disabled = false;
            errorMessage.classList.add("hidden");
        } else {
            generateButton.classList.add("inactive");
            generateButton.classList.remove("active");
            generateButton.disabled = true;
        }
    }

    reportDropdown.addEventListener("change", function () {
        const selectedReport = reportDropdown.value;

        fetch(`/get_report_parameters/${selectedReport}`)
            .then(response => response.text())
            .then(html => {
                reportParametersContainer.innerHTML = html;

                const reportDateInput = document.getElementById("report-date");
                const emailInput = document.getElementById("email");

                reportDateInput.addEventListener("input", updateButtonState);
                emailInput.addEventListener("input", updateButtonState);

                generateButton.addEventListener("click", function () {
                    if (isValidEmail(emailInput.value) && isValidDate(reportDateInput.value)) {
                        errorMessage.classList.add("hidden");

                        // Отправляем данные на сервер
                        fetch("/generate_report", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                                report_type: selectedReport,
                                report_date: reportDateInput.value,
                                email: emailInput.value
                            })
                        })
                        .then(response => {
                            if (response.ok) {
                                return response.json();
                            } else if (response.status === 400) {
                                throw new Error("Некорректные данные. Проверьте и заполните форму заново.");
                            } else {
                                throw new Error("Ошибка сервера. Пожалуйста, попробуйте снова позже.");
                            }
                        })
                        .then(data => {
                            // Обработка успешного ответа
                            if (data.success) {
                                errorMessage.classList.remove("hidden");
                                errorMessage.style.color = "green";
                                errorMessage.textContent = "Отчет формируется и скоро придет на почту.";
                            }
                        })
                        .catch(error => {
                            // Обработка ошибок
                            errorMessage.classList.remove("hidden");
                            errorMessage.style.color = "red";
                            errorMessage.textContent = error.message;
                        });
                    } else {
                        errorMessage.textContent = "Пожалуйста, введите корректные данные.";
                        errorMessage.classList.remove("hidden");
                    }
                });
            })
            .catch(error => {
                console.error("Ошибка загрузки параметров:", error);
            });
    });
});
```

### Шаг 2: Добавление эндпоинта в FastAPI для обработки данных отчета

В `main.py` создадим обработчик для эндпоинта `/generate_report`, который будет принимать параметры отчета, проверять их корректность и возвращать соответствующий ответ.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import date

app = FastAPI()

class ReportRequest(BaseModel):
    report_type: str
    report_date: date
    email: EmailStr

@app.post("/generate_report")
async def generate_report(request: ReportRequest):
    # Проверка типа отчета
    if request.report_type not in ["financial_report", "security_report", "performance_report"]:
        raise HTTPException(status_code=400, detail="Некорректный тип отчета.")

    # Проверка даты
    if request.report_date > date.today():
        raise HTTPException(status_code=400, detail="Дата отчета не может быть в будущем.")

    # Если проверки пройдены, отправляем ответ, что отчет формируется
    # Здесь можно добавить логику для запуска генерации отчета
    return {"success": True, "message": "Отчет формируется и скоро придет на почту."}
```

### Пояснение логики на стороне FastAPI:

1. **Модель `ReportRequest`**: Описывает входные данные, с автоматической проверкой email и даты.
2. **Проверка данных**: Если тип отчета не совпадает с допустимыми значениями или если дата находится в будущем, сервер возвращает ошибку `400` с соответствующим сообщением.
3. **Ответ**: При корректных данных возвращается JSON с полем `success: True`, что означает успешное начало формирования отчета.

### Резюме:

- **Клиентская часть**: Отправляет POST-запрос с параметрами отчета на сервер и выводит сообщения об успешной отправке или об ошибках.
- **Серверная часть**: Выполняет проверку данных и возвращает JSON с результатом в зависимости от корректности введённых данных. 

Теперь при корректном заполнении формы отправляется запрос на сервер, а сервер возвращает сообщение о результате, которое отображается на странице.

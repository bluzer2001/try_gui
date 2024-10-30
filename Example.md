Для этой задачи мы можем использовать JavaScript, чтобы проверять наличие введённых данных и корректность email, а также управлять состоянием кнопки. 

### Шаг 1: Обновление HTML-шаблона

В `index.html` добавим текстовый блок для вывода сообщений об ошибках под формой ввода и стилизуем кнопку для отображения различных состояний:

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

    <!-- Контейнер для параметров отчета -->
    <div id="report-parameters-container"></div>

    <!-- Кнопка для генерации отчета с указанием неактивного состояния -->
    <div class="button-container">
        <button id="generate-report-button" class="inactive" disabled>Показать отчет</button>
    </div>

    <!-- Сообщение об ошибках валидации -->
    <div id="error-message" class="error-message hidden"></div>

    <script src="/static/js/script.js"></script>
</body>
</html>
```

### Шаг 2: CSS для стилизации кнопки и сообщений об ошибках

В `static/css/styles.css` добавим стили для отображения кнопки в различных состояниях и стиля для сообщений об ошибках.

```css
.inactive {
    background-color: rgb(118, 120, 122); /* Серый цвет для неактивного состояния */
    color: #ffffff;
    cursor: not-allowed;
}

.active {
    background-color: rgb(139, 197, 64); /* Зеленый цвет для активного состояния */
    color: #ffffff;
    cursor: pointer;
}

.error-message {
    color: red;
    font-size: 14px;
    margin-top: 10px;
}

.hidden {
    display: none;
}
```

### Шаг 3: JavaScript для активации кнопки и валидации данных

В файле `static/js/script.js` добавим логику, чтобы отслеживать заполнение полей и валидацию email и даты, после чего обновлять состояние кнопки.

```javascript
document.addEventListener("DOMContentLoaded", function () {
    const reportDropdown = document.getElementById("report-dropdown");
    const reportParametersContainer = document.getElementById("report-parameters-container");
    const generateButton = document.getElementById("generate-report-button");
    const errorMessage = document.getElementById("error-message");

    // Функция проверки ввода email
    function isValidEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }

    // Функция проверки ввода даты
    function isValidDate(date) {
        return date !== "";
    }

    // Функция активации кнопки
    function updateButtonState() {
        const reportDate = document.getElementById("report-date")?.value || "";
        const email = document.getElementById("email")?.value || "";

        if (isValidEmail(email) && isValidDate(reportDate)) {
            generateButton.classList.add("active");
            generateButton.classList.remove("inactive");
            generateButton.disabled = false;
            errorMessage.classList.add("hidden"); // скрываем ошибку
        } else {
            generateButton.classList.add("inactive");
            generateButton.classList.remove("active");
            generateButton.disabled = true;
        }
    }

    // Загрузка параметров отчета по выбору отчета
    reportDropdown.addEventListener("change", function () {
        const selectedReport = reportDropdown.value;

        fetch(`/get_report_parameters/${selectedReport}`)
            .then(response => response.text())
            .then(html => {
                reportParametersContainer.innerHTML = html;

                // События на полях формы после загрузки параметров
                const reportDateInput = document.getElementById("report-date");
                const emailInput = document.getElementById("email");

                reportDateInput.addEventListener("input", updateButtonState);
                emailInput.addEventListener("input", updateButtonState);

                generateButton.addEventListener("click", function () {
                    if (!isValidEmail(emailInput.value)) {
                        errorMessage.textContent = "Пожалуйста, введите корректный email.";
                        errorMessage.classList.remove("hidden");
                    } else if (!isValidDate(reportDateInput.value)) {
                        errorMessage.textContent = "Пожалуйста, введите корректную дату.";
                        errorMessage.classList.remove("hidden");
                    } else {
                        errorMessage.classList.add("hidden");
                        // Здесь можно вызвать отправку данных на сервер, если валидация пройдена
                        console.log("Форма корректна, можно отправлять данные.");
                    }
                });
            })
            .catch(error => {
                console.error("Ошибка загрузки параметров:", error);
            });
    });
});
```

### Пояснение логики:

1. **Функция `updateButtonState`**: Проверяет, введены ли данные в поле даты и корректный ли email, чтобы обновить состояние кнопки.
2. **Валидация при клике**: После нажатия на кнопку "Показать отчет" проверяет, введены ли корректные данные в полях и выводит сообщение об ошибке, если данные некорректны.
3. **CSS-классы**: При разных состояниях кнопки добавляются и удаляются классы `active` и `inactive`, чтобы менять цвет кнопки. 

Теперь кнопка будет доступна только при корректном вводе данных, и пользователю будет показано сообщение об ошибке, если введены неверные данные.

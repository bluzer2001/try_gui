Понял! Скорее всего, обработчики `reportDateInput` и `emailInput` не находят нужные элементы, потому что их добавление происходит динамически и позднее, чем мы подключаем скрипт. Чтобы убедиться, что скрипт сработает только тогда, когда элементы точно добавлены, добавим проверку наличия элементов и инициализацию обработчиков сразу после подгрузки HTML.

Вот как можно исправить `financial_report.js`, добавив функцию для периодической проверки наличия элементов до их инициализации:

### Обновленный `financial_report.js`

```javascript
function initReportHandlers() {
    const generateButton = document.getElementById("generate-report-button");
    const reportDateInput = document.getElementById("report-date");
    const emailInput = document.getElementById("email");
    const errorMessage = document.getElementById("error-message");

    if (!generateButton || !reportDateInput || !emailInput || !errorMessage) {
        // Повторно проверяем наличие элементов, если они ещё не загружены
        setTimeout(initReportHandlers, 100);
        return;
    }

    function isValidEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }

    function isValidDate(date) {
        return date !== "";
    }

    function updateButtonState() {
        const reportDate = reportDateInput.value || "";
        const email = emailInput.value || "";

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

    reportDateInput.addEventListener("input", updateButtonState);
    emailInput.addEventListener("input", updateButtonState);
    updateButtonState();

    generateButton.addEventListener("click", function () {
        fetch("/generate_report", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                report_type: "financial_report",
                report_date: reportDateInput.value,
                email: emailInput.value
            })
        })
        .then(response => response.json())
        .then(data => {
            errorMessage.classList.remove("hidden");
            if (data.success) {
                errorMessage.style.color = "green";
                errorMessage.textContent = data.message || "Report is being generated.";
            } else {
                errorMessage.style.color = "red";
                errorMessage.textContent = data.message || "Error generating report.";
            }
        })
        .catch(error => {
            errorMessage.classList.remove("hidden");
            errorMessage.style.color = "red";
            errorMessage.textContent = "Server error. Please try again later.";
        });
    });
}

// Запуск функции инициализации обработчиков
initReportHandlers();
```

### Объяснение

1. **`setTimeout(initReportHandlers, 100);`** — Если элементы не найдены (например, они ещё не подгрузились), функция повторяет проверку через 100 мс до тех пор, пока все элементы не будут готовы.
2. **`initReportHandlers`** — Основная функция для инициализации обработчиков событий, которая начинает работу только тогда, когда все элементы на месте.

Для динамической подгрузки JavaScript файлов можно использовать JavaScript-методы для создания и добавления новых `<script>` элементов в DOM. Например, при выборе определенного отчета мы можем загружать связанный с ним скрипт, который будет содержать необходимую логику.

Вот пошаговое руководство по реализации этого подхода:

### Шаг 1: Структурируем проект

1. В папке `static/js/` создадим отдельные файлы JavaScript для каждого отчета:
    - `static/js/financial_report.js`
    - `static/js/security_report.js`
    - `static/js/performance_report.js`

2. В каждом из этих файлов добавим специфическую логику, необходимую для конкретного отчета.

### Шаг 2: Напишем функцию для динамической загрузки скриптов

Добавим в `static/js/script.js` функцию для подгрузки скриптов. Функция `loadScript` будет добавлять новый `<script>` элемент с указанным URL, а перед этим удалять старые скрипты для предотвращения дублирования.

```javascript
function loadScript(url) {
    // Удаляем предыдущие скрипты отчета
    const existingScript = document.getElementById("report-specific-script");
    if (existingScript) {
        existingScript.remove();
    }

    // Создаем и подключаем новый скрипт
    const script = document.createElement("script");
    script.src = url;
    script.id = "report-specific-script";
    script.defer = true;  // Добавляем defer, чтобы скрипт загружался после парсинга HTML
    document.body.appendChild(script);
}
```

### Шаг 3: Загрузка скрипта при выборе отчета

В обработчике выбора отчета из выпадающего списка добавим вызов `loadScript`, который будет загружать нужный скрипт в зависимости от выбранного отчета.

```javascript
reportDropdown.addEventListener("change", function () {
    const selectedReport = reportDropdown.value;

    fetch(`/get_report_parameters/${selectedReport}`)
        .then(response => response.text())
        .then(html => {
            reportParametersContainer.innerHTML = html;

            // Загрузка специфичного для отчета JavaScript файла
            let scriptUrl = "";
            if (selectedReport === "financial_report") {
                scriptUrl = "/static/js/financial_report.js";
            } else if (selectedReport === "security_report") {
                scriptUrl = "/static/js/security_report.js";
            } else if (selectedReport === "performance_report") {
                scriptUrl = "/static/js/performance_report.js";
            }

            // Загрузка скрипта
            if (scriptUrl) {
                loadScript(scriptUrl);
            }

            // Подключаем обработчики для параметров отчета
            const reportDateInput = document.getElementById("report-date");
            const emailInput = document.getElementById("email");

            reportDateInput.addEventListener("input", updateButtonState);
            emailInput.addEventListener("input", updateButtonState);
        })
        .catch(error => {
            console.error("Ошибка загрузки параметров:", error);
        });
});
```

### Шаг 4: Добавляем логику в файлы отчетов

Пример содержимого `financial_report.js`, где вы можете определить специфическую логику для каждого отчета:

```javascript
// Логика для финансового отчета
document.addEventListener("DOMContentLoaded", function () {
    console.log("Скрипт для финансового отчета загружен");
    
    // Добавьте специфические обработчики для финансового отчета
    // Например, валидация для полей финансового отчета
});
```

Каждый JavaScript файл для отчета (`security_report.js`, `performance_report.js`) может содержать аналогичную структуру, но с уникальной логикой, соответствующей конкретному отчету.

### Резюме

Теперь, при выборе отчета, будет динамически загружаться связанный с ним JavaScript файл. Эта реализация позволит хранить и управлять кодом каждого отчета в отдельном файле, что делает код более чистым и легко расширяемым.

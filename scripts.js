document.addEventListener("DOMContentLoaded", function () {
    const reportDropdown = document.getElementById("report-dropdown");
    const generateButton = document.getElementById("generate-report-button");
    const loadingIndicator = document.getElementById("loading-indicator");
    const reportOutput = document.getElementById("report-output");

    // Включаем кнопку, когда выбран отчет
    reportDropdown.addEventListener("change", function () {
        generateButton.disabled = false;
    });

    // Обработчик клика по кнопке "Показать отчет"
    generateButton.addEventListener("click", function () {
        // Показываем индикатор загрузки
        loadingIndicator.classList.remove("hidden");

        // Деактивируем кнопку, чтобы предотвратить повторные нажатия
        generateButton.disabled = true;

        // Получаем выбранный отчет
        const selectedReport = reportDropdown.value;

        // Отправляем запрос на сервер
        fetch("/generate_report", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ report_type: selectedReport })
        })
        .then(response => response.json())
        .then(data => {
            // Убираем индикатор загрузки
            loadingIndicator.classList.add("hidden");

            // Отображаем результат отчета
            reportOutput.innerHTML = `<p>${data.message}</p>`;

            // Включаем кнопку снова
            generateButton.disabled = false;
        })
        .catch(error => {
            console.error("Ошибка:", error);
            loadingIndicator.classList.add("hidden");
            reportOutput.innerHTML = `<p>Ошибка при генерации отчета.</p>`;
            generateButton.disabled = false;
        });
    });
});

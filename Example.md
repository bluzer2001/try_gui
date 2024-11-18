Here's the backend code for testing the client side. Now I'll provide the relevant code for your static files (`HTML`, `CSS`, and `JavaScript`), as well as the project structure.

### Project Structure
```
project-root/
├── app/
│   ├── main.py
│
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── script.js
│       └── cb_readiness.js
│
└── templates/
    ├── index.html
    └── report_parameters.html
```

### HTML (index.html)
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
 
    <div class="dropdown-container">
        <select id="report-dropdown">
            <option value="" disabled selected>Выберите отчет</option>
            <option value="cb_readiness">ЦБ стройготовность</option>
        </select>
    </div>
 
    <div id="report-parameters-container"></div>
 
    <div class="button-container">
        <button id="generate-report-button" class="inactive" disabled>Показать отчет</button>
    </div>
 
    <div id="error-message" class="error-message">Заполните параметры</div>
    <div id="loading-spinner" class="spinner hidden"></div>
 
    <script src="/static/js/script.js"></script>
</body>
</html>
```

### HTML (report_parameters.html)
```html
<div id="report-parameters">
    <h3>Задайте дату отчета и почту. <br> На эту почту придет эксель с отчетом (только внутренние адреса).</h3>
    <div>
        <label for="report-date">Отчетная дата:</label>
        <input type="date" id="report-date">
    </div>
    <div>
        <label for="email">Электронная почта:</label>
        <input type="email" id="email" placeholder="Введите вашу почту">
    </div>
    <script src="/static/js/cb_readiness.js"></script>
</div>
```

### CSS (styles.css)
```css
body {
    font-family: Arial, sans-serif;
    margin: 20px;
}

h1 {
    text-align: center;
    color: #333;
}

.dropdown-container,
.button-container {
    margin: 20px auto;
    text-align: center;
}

#report-parameters {
    margin: 20px;
}

button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}

button.inactive {
    background-color: #ccc;
    color: #666;
    cursor: not-allowed;
}

button.active {
    background-color: #4CAF50;
    color: white;
}

.error-message {
    color: red;
    text-align: center;
    display: none;
}

.spinner {
    margin: 20px auto;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
}

.hidden {
    display: none;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

### JavaScript (script.js)
```js
document.addEventListener('DOMContentLoaded', () => {
    const reportDropdown = document.getElementById('report-dropdown');
    const reportParametersContainer = document.getElementById('report-parameters-container');
    const generateReportButton = document.getElementById('generate-report-button');
    const errorMessage = document.getElementById('error-message');
    const loadingSpinner = document.getElementById('loading-spinner');

    reportDropdown.addEventListener('change', (event) => {
        const selectedValue = event.target.value;
        if (selectedValue === 'cb_readiness') {
            fetch('/templates/report_parameters.html')
                .then(response => response.text())
                .then(html => {
                    reportParametersContainer.innerHTML = html;
                    const reportDateInput = document.getElementById('report-date');
                    const emailInput = document.getElementById('email');
                    
                    [reportDateInput, emailInput].forEach(input => {
                        input.addEventListener('input', () => {
                            if (reportDateInput.value && emailInput.value) {
                                generateReportButton.classList.remove('inactive');
                                generateReportButton.classList.add('active');
                                generateReportButton.disabled = false;
                            } else {
                                generateReportButton.classList.remove('active');
                                generateReportButton.classList.add('inactive');
                                generateReportButton.disabled = true;
                            }
                        });
                    });
                });
        }
    });

    generateReportButton.addEventListener('click', () => {
        const reportDate = document.getElementById('report-date').value;
        const email = document.getElementById('email').value;
        if (reportDate && email) {
            errorMessage.style.display = 'none';
            loadingSpinner.classList.remove('hidden');
            
            fetch('/generate_report/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `email=${encodeURIComponent(email)}&report_date=${encodeURIComponent(reportDate)}`
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                loadingSpinner.classList.add('hidden');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ошибка сервера. Пожалуйста, попробуйте еще раз.');
                loadingSpinner.classList.add('hidden');
            });
        } else {
            errorMessage.style.display = 'block';
        }
    });
});
```

Copy this code into your project and test it. Let me know if you need further assistance!

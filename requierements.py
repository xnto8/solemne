/index.html
/styles.css
/js/app.js
/js/chart.js
/js/ui.js
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualización de Países</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <h1>Visualización de Datos de Países</h1>
        <div>
            <label for="dataSelector">Seleccionar dato:</label>
            <select id="dataSelector">
                <option value="population">Población</option>
                <option value="area">Área</option>
                <option value="languages">Lenguajes</option>
            </select>
        </div>
        <div>
            <label for="chartType">Seleccionar tipo de gráfico:</label>
            <select id="chartType">
                <option value="bar">Gráfico de barras</option>
                <option value="line">Gráfico de líneas</option>
                <option value="pie">Gráfico de torta</option>
            </select>
        </div>
        <button id="loadData">Cargar Datos</button>
        
        <!-- Cargador de datos -->
        <div id="loader" class="loader" style="display: none;">Cargando...</div>

        <!-- Canvas para el gráfico -->
        <canvas id="countryChart"></canvas>

        <!-- Mensaje de error -->
        <div id="errorMessage" class="error-message" style="display: none;">Hubo un error al cargar los datos. Intenta nuevamente.</div>
    </div>

    <script src="js/ui.js"></script>
    <script src="js/chart.js"></script>
    <script src="js/app.js"></script>
</body>
</html>
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}

.container {
    text-align: center;
    width: 80%;
    max-width: 800px;
}

select {
    padding: 8px;
    margin: 10px;
}

canvas {
    width: 100%;
    height: 400px;
    margin-top: 20px;
}

.loader {
    font-size: 18px;
    color: #007bff;
    font-weight: bold;
}

.error-message {
    color: red;
    font-weight: bold;
}

button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}
// Mostrar el cargador
function showLoader() {
    document.getElementById('loader').style.display = 'block';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('countryChart').style.display = 'none';
}

// Ocultar el cargador
function hideLoader() {
    document.getElementById('loader').style.display = 'none';
    document.getElementById('countryChart').style.display = 'block';
}

// Mostrar mensaje de error
function showError() {
    document.getElementById('errorMessage').style.display = 'block';
}
// Generar gráfico
function generateChart(labels, data, chartType, selectedData) {
    const ctx = document.getElementById('countryChart').getContext('2d');

    // Eliminar gráfico anterior si existe
    if (window.chartInstance) {
        window.chartInstance.destroy();
    }

    window.chartInstance = new Chart(ctx, {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: `${selectedData.charAt(0).toUpperCase() + selectedData.slice(1)} de Países`,
                data: data,
                backgroundColor: chartType === 'pie' ? generateRandomColors(data.length) : 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: chartType !== 'pie' ? {
                y: {
                    beginAtZero: true
                }
            } : {},
            responsive: true
        }
    });
}

// Función para generar colores aleatorios para el gráfico de torta
function generateRandomColors(num) {
    const colors = [];
    for (let i = 0; i < num; i++) {
        const color = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.7)`;
        colors.push(color);
    }
    return colors;
}
document.getElementById('loadData').addEventListener('click', async () => {
    const selectedData = document.getElementById('dataSelector').value;
    const selectedChart = document.getElementById('chartType').value;

    showLoader();

    try {
        const response = await fetch('https://restcountries.com/v3.1/all');
        const countries = await response.json();

        const countryNames = [];
        const countryData = [];

        countries.forEach(country => {
            const name = country.name.common;
            let dataValue = 0;

            switch (selectedData) {
                case 'population':
                    dataValue = country.population || 0;
                    break;
                case 'area':
                    dataValue = country.area || 0;
                    break;
                case 'languages':
                    dataValue = Object.keys(country.languages || {}).length || 0;
                    break;
            }

            countryNames.push(name);
            countryData.push(dataValue);
        });

        // Limitar a los primeros 10 países
        countryNames.splice(10);
        countryData.splice(10);

        // Generar gráfico
        generateChart(countryNames, countryData, selectedChart, selectedData);
        hideLoader();
    } catch (error) {
        console.error('Error al cargar los datos', error);
        showError();
        hideLoader();
    }
});

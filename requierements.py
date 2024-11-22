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
        <canvas id="countryChart"></canvas>
    </div>

    <script src="app.js"></script>
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

canvas {
    width: 100%;
    height: 400px;
    margin-top: 20px;
}

select {
    padding: 8px;
    margin: 10px;
}
document.getElementById('loadData').addEventListener('click', async () => {
    // Obtener los valores seleccionados por el usuario
    const selectedData = document.getElementById('dataSelector').value;
    const selectedChart = document.getElementById('chartType').value;
    
    // Obtener los datos de la API
    const response = await fetch('https://restcountries.com/v3.1/all');
    const countries = await response.json();

    // Preparar los datos para el gráfico
    const countryNames = [];
    const countryData = [];

    countries.forEach(country => {
        const name = country.name.common;
        let dataValue = 0;

        // Obtener el dato correspondiente según la selección
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

    // Limitar los resultados a los primeros 10 países para no saturar el gráfico
    countryNames.splice(10);
    countryData.splice(10);

    // Generar el gráfico con la función correspondiente
    generateChart(countryNames, countryData, selectedChart, selectedData);
});

function generateChart(labels, data, chartType, selectedData) {
    const ctx = document.getElementById('countryChart').getContext('2d');

    // Eliminar el gráfico anterior si existe
    if (window.chartInstance) {
        window.chartInstance.destroy();
    }

    // Crear el gráfico según el tipo seleccionado
    window.chartInstance = new Chart(ctx, {
        type: chartType, // Tipo de gráfico
        data: {
            labels: labels,  // Nombres de los países
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

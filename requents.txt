<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Datos de Países - Visualización</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <h1>Datos de Países</h1>
        <div>
            <label for="dataSelector">Seleccionar dato:</label>
            <select id="dataSelector">
                <option value="population">Población</option>
                <option value="area">Área</option>
                <option value="languages">Lenguajes</option>
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
    max-width: 600px;
}

canvas {
    width: 100%;
    height: 400px;
    margin-top: 20px;
}
document.getElementById('loadData').addEventListener('click', async () => {
    // Obtener el valor seleccionado
    const selectedData = document.getElementById('dataSelector').value;
    
    // Obtener los datos de la API
    const response = await fetch('https://restcountries.com/v3.1/all');
    const countries = await response.json();
    
    // Preparar los datos
    const countryNames = [];
    const countryData = [];

    countries.forEach(country => {
        const name = country.name.common;
        let dataValue = 0;

        // Definir qué dato mostrar dependiendo de la selección del usuario
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

    // Generar gráfico
    generateChart(countryNames, countryData, selectedData);
});

function generateChart(labels, data, selectedData) {
    const ctx = document.getElementById('countryChart').getContext('2d');

    // Eliminar el gráfico anterior si existe
    if (window.chartInstance) {
        window.chartInstance.destroy();
    }

    // Crear un nuevo gráfico
    window.chartInstance = new Chart(ctx, {
        type: 'bar',  // Tipo de gráfico (barra)
        data: {
            labels: labels.slice(0, 10),  // Mostrar solo los 10 primeros países para evitar saturar la pantalla
            datasets: [{
                label: `${selectedData.charAt(0).toUpperCase() + selectedData.slice(1)} de Países`,
                data: data.slice(0, 10),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}


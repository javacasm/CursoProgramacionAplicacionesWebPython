document.getElementById('pizzaForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Obtener valores del formulario
    const formData = new FormData(this);
    
    // Validación básica en el frontend
    const inputs = ['diam_familiar', 'price_familiar', 'diam_mediana', 'price_mediana', 'border_width'];
    let valid = true;
    inputs.forEach(input => {
        const value = formData.get(input);
        if (!value || isNaN(value) || value < 0) {
            valid = false;
        }
    });
    
    if (!valid) {
        showError('Por favor, complete todos los campos con valores numéricos no negativos.');
        return;
    }
    
    // Enviar solicitud al servidor
    fetch('/calculate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
        } else {
            showResult(data.result);
        }
    })
    .catch(error => {
        showError('Error en el servidor. Inténtelo de nuevo.');
        console.error(error);
    });
});

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('d-none');
    document.getElementById('result').classList.add('d-none');
}

function showResult(result) {
    const resultDiv = document.getElementById('result-content');
    resultDiv.innerHTML = `
        <h5>Con bordes incluidos:</h5>
        <p>Área Familiar: ${result.area_fam} cm², Costo por cm²: ${result.cost_per_cm2_fam} €/cm²</p>
        <p>Área Mediana: ${result.area_med} cm², Costo por cm²: ${result.cost_per_cm2_med} €/cm²</p>
        <p><strong>Pizza más rentable: ${result.most_profitable}</strong></p>
        <h5 class="mt-3">Sin bordes (borde de ${result.border} cm):</h5>
        <p>Área Familiar: ${result.area_fam_no_border} cm², Costo por cm²: ${result.cost_per_cm2_fam_no_border}</p>
        <p>Área Mediana: ${result.area_med_no_border} cm², Costo por cm²: ${result.cost_per_cm2_med_no_border}</p>
        <p><strong>Pizza más rentable: ${result.most_profitable_no_border}</strong></p>
        <h5 class="mt-3">Consideraciones:</h5>
        <ul>
            <li>Asegúrate de que la cantidad sea adecuada para evitar desperdicio.</li>
            <li>Verifica si hay diferencias en ingredientes o promociones.</li>
        </ul>
    `;
    document.getElementById('result').classList.remove('d-none');
    document.getElementById('error').classList.add('d-none');
}

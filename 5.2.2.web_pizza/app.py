from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def validate_inputs(diam_fam, price_fam, diam_med, price_med, border):
    try:
        diam_fam = float(diam_fam)
        price_fam = float(price_fam)
        diam_med = float(diam_med)
        price_med = float(price_med)
        border = float(border)
        
        if diam_fam <= 0 or price_fam <= 0 or diam_med <= 0 or price_med <= 0:
            return None, "Los diámetros y precios deben ser mayores que cero."
        if border < 0:
            return None, "El ancho del borde no puede ser negativo."
        if border * 2 >= diam_fam or border * 2 >= diam_med:
            return None, "El borde es demasiado ancho para el diámetro de la pizza."
        
        return (diam_fam, price_fam, diam_med, price_med, border), None
    except ValueError:
        return None, "Por favor, ingrese valores numéricos válidos."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Obtener datos del formulario
    diam_fam = request.form.get('diam_familiar')
    price_fam = request.form.get('price_familiar')
    diam_med = request.form.get('diam_mediana')
    price_med = request.form.get('price_mediana')
    border = request.form.get('border_width', '2.0')  # Valor por defecto: 2 cm
    
    # Validar entradas
    inputs, error = validate_inputs(diam_fam, price_fam, diam_med, price_med, border)
    if error:
        return jsonify({'error': error})
    
    diam_fam, price_fam, diam_med, price_med, border = inputs
    
    # Calcular áreas totales
    area_fam = math.pi * (diam_fam / 2) ** 2
    area_med = math.pi * (diam_med / 2) ** 2
    
    # Calcular costos por cm² (con bordes)
    cost_per_cm2_fam = price_fam / area_fam
    cost_per_cm2_med = price_med / area_med
    
    # Calcular áreas sin bordes
    diam_fam_no_border = diam_fam - 2 * border
    diam_med_no_border = diam_med - 2 * border
    area_fam_no_border = math.pi * (diam_fam_no_border / 2) ** 2 if diam_fam_no_border > 0 else 0
    area_med_no_border = math.pi * (diam_med_no_border / 2) ** 2 if diam_med_no_border > 0 else 0
    
    # Calcular costos por cm² (sin bordes)
    cost_per_cm2_fam_no_border = price_fam / area_fam_no_border if area_fam_no_border > 0 else float('inf')
    cost_per_cm2_med_no_border = price_med / area_med_no_border if area_med_no_border > 0 else float('inf')
    
    # Determinar cuál es más rentable
    most_profitable = "Familiar" if cost_per_cm2_fam < cost_per_cm2_med else "Mediana"
    most_profitable_no_border = "Familiar" if cost_per_cm2_fam_no_border < cost_per_cm2_med_no_border else "Mediana"
    
    # Formatear resultados
    result = {
        'area_fam': round(area_fam, 2),
        'cost_per_cm2_fam': round(cost_per_cm2_fam, 5),
        'area_med': round(area_med, 2),
        'cost_per_cm2_med': round(cost_per_cm2_med, 5),
        'most_profitable': most_profitable,
        'area_fam_no_border': round(area_fam_no_border, 2),
        'cost_per_cm2_fam_no_border': round(cost_per_cm2_fam_no_border, 5) if area_fam_no_border > 0 else 'N/A',
        'area_med_no_border': round(area_med_no_border, 2),
        'cost_per_cm2_med_no_border': round(cost_per_cm2_med_no_border, 5) if area_med_no_border > 0 else 'N/A',
        'most_profitable_no_border': most_profitable_no_border,
        'border': border
    }
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request

app = Flask(__name__)

# Emission Factors (kg CO2 per unit)
# Sources: EPA / Department for Business, Energy & Industrial Strategy
FACTORS = {
    "electricity": 0.4,   # per kWh
    "gas": 5.3,           # per Therm
    "fuel": 2.3,          # per Liter of Petrol
    "distance": 0.15      # per km Flown
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get Inputs from Form
        e_val = float(request.form.get('electricity', 0))
        g_val = float(request.form.get('gas', 0))
        f_val = float(request.form.get('fuel', 0))
        d_val = float(request.form.get('distance', 0))

        # Calculate individual footprints
        breakdown = {
            "Electricity": e_val * FACTORS["electricity"],
            "Heating (Gas)": g_val * FACTORS["gas"],
            "Transport (Fuel)": f_val * FACTORS["fuel"],
            "Travel (Flights)": d_val * FACTORS["distance"]
        }

        total = sum(breakdown.values())
        
        # Identify the "Worst Offender"
        highest_category = max(breakdown, key=breakdown.get)

        # Logic-based Reduction Tips
        tips_library = {
            "Electricity": [
                "Switch off lights and electrical appliances when not using them.",
"Switch to energy-saving LED light globes.",
"Shut doors and close curtains.",
"Save energy in how you wash and dry clothes.",
"Understand and improve your home's energy use.",
"Save energy in the kitchen."
            ],
            "Heating (Gas)": [
                "Seal gaps in windows and doors with weatherstripping.",
                "Lower your water heater temperature to 48°C (120°F).",
                "Install a programmable thermostat to optimize heating."
            ],
            "Transport (Fuel)": [
                "Check tire pressure; under-inflated tires waste fuel.",
                "Remove heavy roof racks when not in use to improve aerodynamics.",
                "Consider carpooling or using public transit for work commutes."
            ],
            "Travel (Flights)": [
                "Fly Economy: Business class has 3x the carbon footprint.",
                "Pack light: Heavier planes burn more fuel.",
                "Offset your carbon through certified reforestation projects."
            ]
        }

        return render_template('index.html', 
                               result=round(total, 2), 
                               top_source=highest_category,
                               tips=tips_library[highest_category],
                               inputs={'e': e_val, 'g': g_val, 'f': f_val, 'd': d_val})
    
    except ValueError:
        return render_template('index.html', error="Invalid input. Please enter numbers only.")

if __name__ == '__main__':
    app.run(debug=True)
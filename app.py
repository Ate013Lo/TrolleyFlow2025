import pandas as pd
import numpy as np
import json
from flask import Flask, request, jsonify

# ===================================================================
# CONFIGURACIÓN E INICIALIZACIÓN
# ===================================================================
app = Flask(__name__)
DATA_FILE = 'Alcohol_gemini.csv'
df_historico = pd.DataFrame() # Initialize empty DataFrame

# ===================================================================
# 1. FUNCIÓN DE CARGA Y TRANSFORMACIÓN DE DATOS
#    Se ejecuta al iniciar la aplicación para pre-procesar el CSV.
# ===================================================================
def load_and_transform_data():
    """
    Loads the historical data and performs required data engineering transformations.
    This function should only run once at application startup.
    """
    global df_historico
    print(f"Loading and processing data from: {DATA_FILE}...")
    
    try:
        # Load the raw CSV file. Added 'encoding' parameter to handle non-UTF8 characters.
        df = pd.read_csv(DATA_FILE, encoding='latin-1') 
    except FileNotFoundError:
        # Critical error: The file is missing
        print(f"\nFATAL ERROR: Data file '{DATA_FILE}' NOT FOUND. Please ensure the file is in the same directory as app.py.")
        return pd.DataFrame()
    except Exception as e:
        print(f"\nFATAL ERROR: An unexpected error occurred during data loading: {e}")
        return pd.DataFrame()
    
    # --- 1.0 Limpieza de Datos CRÍTICA: Eliminar caracteres no numéricos ---
    # El error indica que 'Fill_Level' contiene '%' y no se puede convertir a float.
    try:
        # 1. Elimina el carácter '%' (y posibles espacios en blanco) de la columna
        df['Fill_Level'] = df['Fill_Level'].astype(str).str.replace('%', '', regex=False).str.strip()
        
        # 2. Convierte la columna a float (si hay valores vacíos o NaN, se mantienen como NaN)
        df['Fill_Level'] = pd.to_numeric(df['Fill_Level'], errors='coerce')

        # 3. Rellena los NaN resultantes con 0 (ya que se usa en el cálculo de consumo)
        df['Fill_Level'] = df['Fill_Level'].fillna(0.0)

    except Exception as e:
        print(f"\nFATAL ERROR: Failed during Fill_Level cleaning/conversion: {e}")
        return pd.DataFrame()


    # --- 1.1 Transformación de Consumo ---
    # Create 'Consumo_pct': 100 - Fill_Level if Opened/Resealed, else 0
    df['Consumo_pct'] = np.where(
        df['Seal_Status'].isin(['Opened', 'Resealed']),
        100 - df['Fill_Level'].astype(float),
        0.0
    )

    # Create 'Consumo_ml': (Bottle_Size * Consumo_pct) / 100
    df['Consumo_ml'] = (df['Bottle_Size'].fillna(0) * df['Consumo_pct']) / 100

    # --- 1.2 Transformación de Ruta y Categorías ---
    # Create 'Ruta': Origin-Destination
    df['Ruta'] = df['Origin'].astype(str) + '-' + df['Destination'].astype(str)
    
    # Clean up column names and types for filtering
    df['Inbound_Flight'] = df['Inbound_Flight'].astype(str).str.upper()
    df['Service_Class'] = df['Service_Class'].astype(str)
    df['Brand'] = df['Brand'].astype(str)
    # Ensure Category is also a string for grouping (NEW)
    df['Category'] = df['Category'].astype(str).str.strip() 
    
    print(f"Data processing complete. {len(df)} records loaded.")
    return df

# Carga global del DataFrame
df_historico = load_and_transform_data()


# ===================================================================
# 2. MOTOR DE PRONÓSTICO (Lógica de Nivel 3: Incluye Agregación por Categoría)
# ===================================================================

def post_process_and_aggregate(detailed_forecast_list):
    """
    Takes the detailed forecast and aggregates the predicted bottles needed 
    by product Category for the front-end display.
    """
    df_forecast = pd.DataFrame(detailed_forecast_list)
    
    # CORRECCIÓN: Usar 'Category' con C mayúscula, ya que es como se genera en la lista.
    summary = df_forecast.groupby('Category').agg(
        total_bottles_needed=('predicted_bottles_needed', 'sum')
    ).reset_index()
    
    # Renombramos la columna 'Category' a 'category' (minúsculas) para el output JSON si es necesario, 
    # pero el problema inicial era el .groupby()
    summary.columns = ['category', 'total_bottles_needed']
    
    return summary.to_dict(orient='records')


def calculate_level3_forecast(dataframe, flight_number, service_class=None):
    """
    Calculates the bottle consumption forecast based on historical averages (Level 3 Model).
    Filters by Inbound_Flight AND Route, and includes Category in the prediction output.
    """
    # ------------------
    # 2.1 Encontrar la Ruta Actual
    # ------------------
    route_data = dataframe.query(f"Inbound_Flight == '{flight_number.upper()}'")
    
    if route_data.empty:
        return None, 0
    
    current_route = route_data['Ruta'].mode().iloc[0]

    # ------------------
    # 2.2 Filtrado de Datos (Vuelo, Ruta y Clase de Servicio)
    # ------------------
    query_filter = f"Inbound_Flight == '{flight_number.upper()}' and Ruta == '{current_route}'"
    if service_class:
        query_filter += f" and Service_Class == '{service_class}'"
    
    df_filtered = dataframe.query(query_filter) 
    
    # Fallback: Si el filtro estricto no encuentra datos, ignoramos la clase de servicio
    if df_filtered.empty and service_class:
        query_filter_fallback = f"Inbound_Flight == '{flight_number.upper()}' and Ruta == '{current_route}'"
        df_filtered = dataframe.query(query_filter_fallback)
        print(f"DEBUG: No data for {flight_number} in {service_class} on {current_route}. Falling back to general route data.")
    
    if df_filtered.empty:
        return None, 0

    # ------------------
    # 2.3 Agregación de Datos
    # ------------------
    # Group by Category, Brand, and Bottle_Size (NEW: Added 'Category')
    forecast_agg = df_filtered.groupby(['Category', 'Brand', 'Bottle_Size']).agg(
        predicted_consumption_ml=('Consumo_ml', 'mean'),
        historical_records=('Bottle_ID', 'count')
    ).reset_index()

    # ------------------
    # 2.4 Cálculo Final y Confianza
    # ------------------
    
    # Calculate bottles needed (ceil(consumption / size))
    forecast_agg['predicted_bottles_needed'] = np.ceil(
        forecast_agg['predicted_consumption_ml'] / forecast_agg['Bottle_Size']
    ).astype(int)

    # Simple Confidence Metric based on data volume
    forecast_agg['confidence'] = forecast_agg['historical_records'].apply(
        lambda x: 'High' if x >= 10 else ('Medium' if x >= 3 else 'Low')
    )
    
    # Prepare the forecast list for JSON output
    # IMPORTANT: Ensure Category column is included
    forecast_list = forecast_agg.rename(columns={'Bottle_Size': 'bottle_size_ml'}).to_dict(orient='records')

    # Prepare flight details summary
    flight_details = {
        "flight_number": flight_number,
        "service_class": service_class,
        "historical_data_points_found": len(df_filtered),
        "route_used_for_forecast": current_route
    }

    return flight_details, forecast_list


# ===================================================================
# 3. ENDPOINTS DE LA API (Flask Routes)
# ===================================================================

@app.route('/api/v1/forecast/bottles', methods=['GET'])
def get_bottle_forecast():
    """
    RESTful API endpoint to get the predicted bottle forecast for a specific flight.
    Now using the Level 3 forecast model (includes Category aggregation).
    """
    
    if df_historico.empty:
         return jsonify({
            "error": "Internal Server Error",
            "message": "Historical data failed to load. Check the console logs for 'FATAL ERROR'."
        }), 500

    # Get query parameters
    # The request can come from the local IP (simulating ngrok) or an actual ngrok tunnel
    flight_number = request.args.get('flight_number')
    service_class = request.args.get('service_class')

    if not flight_number:
        return jsonify({
            "error": "Missing Parameter",
            "message": "The 'flight_number' parameter is mandatory."
        }), 400

    # Call the forecast engine (Level 3)
    flight_details, detailed_forecast = calculate_level3_forecast(
        df_historico, 
        flight_number, 
        service_class
    )

    # Check if the forecast found any data
    if flight_details is None:
        return jsonify({
            "flight_details": {
                "flight_number": flight_number,
                "service_class": service_class,
                "historical_data_points_found": 0,
                "route_used_for_forecast": "N/A"
            },
            "message": "No specific historical data found for the provided parameters.",
            "forecast_summary_by_category": [],
            "detailed_forecast_by_brand": []
        }), 200

    # Aggregate results for the UI display
    forecast_summary = post_process_and_aggregate(detailed_forecast)


    # Construct the final JSON response
    response = {
        "flight_details": flight_details,
        "forecast_summary_by_category": forecast_summary, # Summary for the front-end UI
        "detailed_forecast_by_brand": detailed_forecast    # Detailed list for inventory
    }
    
    return jsonify(response), 200

@app.route('/get_url', methods=['GET'])
def get_simulated_url():
    """
    NEW ENDPOINT to return a simulated external URL to bypass ngrok issues for local testing.
    The client application should use the 'simulated_url' as the base API path.
    """
    
    simulated_base_url = "http://127.0.0.1:5000"
    
    return jsonify({
        "status": "Success",
        "message": "Use the 'simulated_url_endpoint' in your C# application as the base URL to bypass ngrok/firewall problems.",
        "simulated_url_endpoint": simulated_base_url + "/api/v1/forecast/bottles?flight_number={FLIGHT_CODE}&service_class={SERVICE_CLASS_CODE}",
        "example_url": simulated_base_url + "/api/v1/forecast/bottles?flight_number=BA370&service_class=First"
    }), 200


@app.route('/status', methods=['GET'])
def get_status():
    """
    Health check endpoint to verify the API is running and data is loaded.
    """
    data_loaded = not df_historico.empty
    
    if data_loaded:
        status_code = 200
        message = "API is running and historical data is successfully loaded."
    else:
        status_code = 503
        message = "API is running, but FAILED to load historical data (Alcohol_gemini.csv)."

    return jsonify({
        "status": "OK" if data_loaded else "ERROR",
        "message": message,
        "records_count": len(df_historico)
    }), status_code

# ===================================================================
# EJECUCIÓN DEL SERVIDOR
# ===================================================================
if __name__ == '__main__':
    # Esto ejecuta el servidor en http://0.0.0.0:5000/ (puerto estándar y host universal)
    # Usar debug=True es bueno para el desarrollo
    print("\n--- Starting Flask API Server ---")
    app.run(debug=True, host='0.0.0.0', port=5000)

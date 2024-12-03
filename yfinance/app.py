from datetime import timedelta
from flask import Flask, jsonify, make_response, request, Response, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from prometheus_client import Counter, Histogram, start_http_server, Gauge, generate_latest, CONTENT_TYPE_LATEST
from sklearn.preprocessing import MinMaxScaler
import holidays
import numpy as np
import os
import psutil
import tensorflow as tf
import time
import yfinance as yf


# Criando metricas
REQUEST_COUNT       = Counter('api_request_total',              'Total de requisições recebidas')
REQUEST_DURATION    = Histogram('api_request_duration_seconds', 'Duração das requisições em segundos')
ERROR_COUNT         = Counter('api_error_total',                'Total de erros da API')
CPU_USAGE           = Gauge('system_cpu_usage_percent',         'Percentual de uso da CPU do sistema')
MEMORY_USAGE        = Gauge('system_memory_usage_percent',      'Percentual de uso da memória do sistema')

app = Flask(__name__,static_folder='static')

# Inicia o prometheus
start_http_server(9090)

# Habilitar CORS
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": "*"}})

# Carregar o modelo
model_path = os.path.join('modelo', 'lstm.h5')
model = tf.keras.models.load_model(model_path)

# Configurar swagger
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
swagger_bleprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {"app_name": "API de Previsão de Ativos"}
)
app.register_blueprint(swagger_bleprint, url_prefix=SWAGGER_URL)

# Funcao para coletar metricas do sistema
def collect_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)

# Funcao para gerar as proximos datas uteis
def generate_future_dates(last_date, days):
    br_holidays = holidays.Brazil()  
    future_dates = []
    current_date = last_date
    while len(future_dates) < days:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5 and current_date not in br_holidays:
            future_dates.append(current_date.strftime('%d/%m/%Y'))
    return future_dates

# Funcao para criar as previsoes
def make_prediction(ticker, days=20):

    # Verificar se parametro ja esta no padrao do yfinance
    if not ticker.endswith('.SA'):
        ticker += '.SA'
    
    df = yf.download(ticker, start='2023-01-01')
    df = df[['Close']].dropna() 

    # Verificar se ha dados
    if df.empty:
        raise ValueError(f"Nenhum dado histórico disponível para o ticker {ticker}")

    # Obter a ultima data disponivel
    last_date = df.index[-1].date()

    # Escalar os dados
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df.values.reshape(-1, 1))  

    # Criar serie para previsao
    SEQ_LENGTH = 50
    last_data = df_scaled[-SEQ_LENGTH:]  
    if len(last_data) < SEQ_LENGTH:
        raise ValueError("Dados insuficientes para criar a sequência de entrada.")

    last_data_reshaped = last_data.reshape((1, SEQ_LENGTH, 1))  # Acertar formato

    # Prever dias
    predictions = []
    for _ in range(days):
        prediction = model.predict(last_data_reshaped, verbose=0)
        predictions.append(prediction[0][0])
        last_data_reshaped = np.append(last_data_reshaped[:, 1:, :], prediction.reshape(1, 1, 1), axis=1)

    # Converter previsoes para escala original
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten().tolist()

    # Gerar as data
    future_dates = generate_future_dates(last_date, days)

    # Retornar JSON
    show_ticker = ticker.replace('.SA', '')
    return {       
        f"Previsao20Dias_{show_ticker}": [
            {
                "Data": date, 
                "Previsao": round(prediction, 2)
            } 
            for date, prediction in zip(future_dates, predictions)
        ]
    }

@app.route('/metrics', methods=['GET'])
def metrics():
    """
    Rota para expor as métricas do Prometheus.
    """
    # Incrementa o contador de requisições
    REQUEST_COUNT.inc()

    try:
        # Gera as métricas e retorna no formato esperado pelo Prometheus
        metrics_data = generate_latest()
        return Response(metrics_data, content_type=CONTENT_TYPE_LATEST)

    except Exception as e:
        ERROR_COUNT.inc()  # Incrementa o contador de erros
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['GET'])
@REQUEST_DURATION.time()
def predict():
    """
    Previsão de preços de ações.
    ---
    parameters:
      - name: ticker
        in: query
        type: string
        required: true
        description: O código do ativo para previsão.
    responses:
      200:
        description: Previsões retornadas com sucesso.
        schema:
          type: object
          properties:
            Previsões:
              type: array
              items:
                type: object
                properties:
                  Data:
                    type: string
                    example: "25/11/2024"
                  Previsão R$:
                    type: number
                    example: 23.45
      500:
        description: Erro no servidor.
    """
    REQUEST_COUNT.inc() # Conta requisicoes
    try:

        # Obter ticker do parametro
        ticker = request.args.get('ticker', 'PETR4') # PETR4 default caso ticker nao seja enviado

        # Fazer previsoes 
        predictions = make_prediction(ticker = ticker)

        # Retornar  JSON
        response = make_response(jsonify(predictions))
        response.headers['Content-Type'] = 'application/json'
        
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route("/swagger.json")
def swagger_json():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'swagger.json')
    
if __name__ == '__main__':
    import threading

    def collect_metrics():
        while True:
            collect_system_metrics()
            time.sleep(10)

    # Iniciar thread para coletar metricas
    threading.Thread(target = collect_metrics, daemon = True).start()
    port = int(os.environ.get('PORT', 8080))  # Porta padrão é 8080
    app.run(host='0.0.0.0', port=port)

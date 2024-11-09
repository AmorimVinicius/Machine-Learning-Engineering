from flask import Flask, jsonify, make_response
import yfinance as yf
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import os

app = Flask(__name__)

# Carregar o modelo
model_path = os.path.join('C:/GIT/Machine-Learning-Engineering/yfinance/modelo', 'lstm.h5')
model = tf.keras.models.load_model(model_path)

# Função para criar as previsões
def make_prediction(ticker='PETR4.SA', days=20):
    # Obter dados históricos
    df = yf.download(ticker, start='2023-01-01')
    df = df[['Close']].dropna()
    
    # Escalar os dados
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df)

    # Criar série para previsão
    SEQ_LENGTH = 50
    last_data = df_scaled[-SEQ_LENGTH:]  # Seleciona as últimas observações para a série inicial

    # Prever vários dias no futuro
    predictions = []
    last_data_reshaped = last_data.reshape((1, SEQ_LENGTH, 1))

    for _ in range(days):
        prediction = model.predict(last_data_reshaped)
        predictions.append(prediction[0][0])
        last_data_reshaped = np.append(last_data_reshaped[:, 1:, :], prediction.reshape(1, 1, 1), axis=1)
    
    # Converter previsões para escala original
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten().tolist()
    
    return {
        "predictions": predictions
    }

@app.route('/predict', methods=['GET']+)
def predict():
    try:
        # Fazer previsões dinamicamente
        predictions = make_prediction()
        
        # Retornar as previsões como JSON
        response = make_response(jsonify(predictions))
        response.headers['Content-Type'] = 'application/json'
        
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

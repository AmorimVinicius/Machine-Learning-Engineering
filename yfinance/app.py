from flask import Flask, jsonify, make_response
import tensorflow as tf
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)

# Carrega o modelo
model_path = os.path.join('C:/GIT/Machine-Learning-Engineering/yfinance/modelo', 'lstm.h5')
model = tf.keras.models.load_model(model_path)

# Função para fazer previsões
def make_prediction():
    # Aqui você chama o método que já existe no seu modelo para gerar as previsões
    predictions = model.predict_future()  # Substitua pelo método correto que gera as previsões
    return {
        "predictions_5_days": predictions[0],
        "predictions_10_days": predictions[1],
        "predictions_15_days": predictions[2],
        "predictions_20_days": predictions[3],
    }

    response = make_response(jsonify(predictions))
    response.headers['Content-Type'] = 'application/json'

@app.route('/predict', methods=['POST'])  # Mantenha o método GET
def predict():
    try:
        # Chama a função de previsão
        predictions = make_prediction()
        
        # Return json
        response = make_response(jsonify(predictions))

        # Define o cabeçalho Content-Type
        response.headers['Content-Type'] = 'application/json'
        
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

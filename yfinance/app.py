from flask import Flask, jsonify
import tensorflow as tf

app = Flask(__name__)

# Carrega o modelo
model = tf.keras.models.load_model('modelo/lstm.h5')

# Função para fazer previsões
def make_prediction():
    # Chama o método de previsão do seu modelo
    predictions = model.predict_future()  # Altere isso para o método correto do seu modelo
    return {
        "predictions_5_days": predictions[0],
        "predictions_10_days": predictions[1],
        "predictions_15_days": predictions[2],
        "predictions_20_days": predictions[3],
    }

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Chama a função de previsão
        predictions = make_prediction()
        
        # Retorna a previsão em formato JSON
        return jsonify(predictions)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

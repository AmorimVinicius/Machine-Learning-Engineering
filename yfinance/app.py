from flask import Flask, request, jsonify
import yfinance as yf
import os

app = Flask(__name__)

# Rota para buscar os dados históricos
@app.route('/api/get_stock_price', methods=['GET'])
def get_stock_price():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'Ação não encontrada'}), 400
    try:
        stock_data = yf.Ticker(ticker)
        historical = stock_data.history(period="5d")

        # Serializar json
        data = historical.reset_index().to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

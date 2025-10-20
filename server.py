from flask import Flask, jsonify
import mercadopago

app = Flask(__name__)

# Coloque seu token do Mercado Pago aqui
sdk = mercadopago.SDK("APP_USR-5699245059856282-101519-9ec457838f1383fe9049e9c4618327b2-555644478")

@app.route('/')
def home():
    return jsonify({"status": "Servidor rodando!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

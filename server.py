from flask import Flask, jsonify, request
import mercadopago
import random

app = Flask(__name__)

# ===== TOKEN MERCADO PAGO =====
sdk = mercadopago.SDK("APP_USR-5699245059856282-101519-9ec457838f1383fe9049e9c4618327b2-555644478")  # coloque seu token aqui

# ===== ROTA PRINCIPAL =====
@app.route('/')
def home():
    return jsonify({"status": "Servidor rodando!"})

# ===== GERAR QR CODE PARA PAGAMENTO =====
@app.route('/gerar_qr', methods=['GET'])
def gerar_qr():
    try:
        # Aqui você cria um pagamento de exemplo (R$ 5,00 por teste)
        preference_data = {
            "items": [
                {
                    "title": "Bebida",
                    "quantity": 1,
                    "unit_price": 5.00
                }
            ],
            "back_urls": {
                "success": "https://bebidas-1.onrender.com/success",
                "failure": "https://bebidas-1.onrender.com/failure",
                "pending": "https://bebidas-1.onrender.com/pending"
            },
            "auto_return": "approved"
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        qr_link = preference["sandbox_init_point"]  # sandbox para testes, depois mudar para init_point

        # Mensagem divertida que muda a cada venda
        mensagens = [
            "Pagamento confirmado! Preparando sua bebida 🍹",
            "Bebida a caminho! 😎",
            "Bebida liberada! Aproveite! 🥳"
        ]
        mensagem = random.choice(mensagens)

        return jsonify({
            "mensagem": mensagem,
            "qr_base64": qr_link  # aqui o ESP32 vai abrir o link ou gerar QR
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ===== ROTAS DE TESTE =====
@app.route('/success')
def success():
    return "Pagamento aprovado! 🍹"

@app.route('/failure')
def failure():
    return "Pagamento falhou 😢"

@app.route('/pending')
def pending():
    return "Pagamento pendente ⏳"

# ===== MAIN =====
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

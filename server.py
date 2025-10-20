from flask import Flask, jsonify, request
import mercadopago
import random

app = Flask(__name__)

# Token Mercado Pago
sdk = mercadopago.SDK("APP_USR-5699245059856282-101519-9ec457838f1383fe9049e9c4618327b2-555644478")

# Mensagens engraçadas que mudam a cada venda
messages = [
    "🍹 Pagamento confirmado! Preparando sua bebida...",
    "🥤 Suco a caminho! Segura o copo!",
    "🍸 Bebida liberada! Aproveite!",
    "🍺 Cheers! Seu pedido tá na bomba!",
    "🍹 Obrigado! Mais uma bebida chegando!"
]

@app.route("/gerar_qr", methods=["POST"])
def gerar_qr():
    # Recebe valor da venda (em centavos)
    data = request.get_json()
    amount = data.get("amount", 100)  # default R$1,00 se não passar

    # Cria preferência no Mercado Pago
    preference_data = {
        "items": [{"title": "Bebida", "quantity": 1, "unit_price": amount / 100}],
        "back_urls": {"success": "https://bebidas-1.onrender.com", "failure": "https://bebidas-1.onrender.com"},
        "auto_return": "approved"
    }
    preference_response = sdk.preference().create(preference_data)
    qr_url = preference_response["response"]["init_point"]

    # Escolhe mensagem engraçada
    msg = random.choice(messages)

    return jsonify({"qr_url": qr_url, "message": msg})

@app.route("/check_payment", methods=["POST"])
def check_payment():
    # Recebe payment_id do ESP32 (Mercado Pago webhook alternativo)
    data = request.get_json()
    payment_id = data.get("payment_id")
    if not payment_id:
        return jsonify({"status": "error", "message": "Sem payment_id"}), 400

    payment = sdk.payment().get(payment_id)
    status = payment["response"]["status"]
    if status == "approved":
        return jsonify({"status": "approved"})
    else:
        return jsonify({"status": status})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

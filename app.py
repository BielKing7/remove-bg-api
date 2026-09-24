import os
from io import BytesIO

import requests
from flask import Flask, request, jsonify, send_file
from PIL import Image
from rembg import remove, new_session

app = Flask(__name__)

# Defina essa variável de ambiente no Render (nunca deixe a chave fixa no código)
API_KEY = os.environ.get("API_KEY", "troque-esta-chave")

# u2netp é o modelo "leve" (~4-5MB) — necessário pro plano free do Render (512MB RAM)
MODEL_NAME = os.environ.get("MODEL_NAME", "u2netp")
_session = new_session(MODEL_NAME)


@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "API pessoal de remoção de fundo está no ar",
        "uso": "GET /remove-bg?url=LINK_DA_IMAGEM  (header x-api-key ou ?api_key=)"
    })


@app.route("/remove-bg", methods=["GET", "POST"])
def remove_bg():
    # --- checa API key ---
    key = request.headers.get("x-api-key") or request.args.get("api_key")
    if request.is_json:
        key = key or (request.json or {}).get("api_key")
    if key != API_KEY:
        return jsonify({"error": "API key inválida ou ausente"}), 401

    # --- pega a URL da imagem ---
    image_url = request.args.get("url")
    if not image_url and request.is_json:
        image_url = (request.json or {}).get("url")
    if not image_url:
        return jsonify({"error": "Parâmetro 'url' é obrigatório"}), 400

    # --- baixa a imagem ---
    try:
        resp = requests.get(image_url, timeout=15)
        resp.raise_for_status()
        input_image = Image.open(BytesIO(resp.content)).convert("RGBA")
    except Exception as e:
        return jsonify({"error": f"Não foi possível baixar a imagem: {e}"}), 400

    # --- remove o fundo ---
    try:
        output_image = remove(input_image, session=_session)
    except Exception as e:
        return jsonify({"error": f"Erro ao remover o fundo: {e}"}), 500

    buf = BytesIO()
    output_image.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png", download_name="sem-fundo.png")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

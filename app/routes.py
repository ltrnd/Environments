from flask import Blueprint, request, jsonify
import os
from datetime import datetime

bp = Blueprint("main", __name__)

comando = {"comando": None}
localizacao = {"latitude": None, "longitude": None, "timestamp": None}

@bp.route("/enviar", methods=["POST"])
def receber_localizacao():
    data = request.get_json()
    localizacao["latitude"] = data.get("latitude")
    localizacao["longitude"] = data.get("longitude")
    localizacao["timestamp"] = data.get("timestamp")
    return jsonify({"status": "ok", "mensagem": "Localização recebida com sucesso!"})

@bp.route("/localizacao", methods=["GET"])
def enviar_localizacao():
    return jsonify(localizacao)

@bp.route("/comando", methods=["GET", "POST"])
def gerenciar_comando():
    if request.method == "POST":
        data = request.get_json()
        comando["comando"] = data.get("comando")
        return jsonify({"status": "ok", "mensagem": "Comando atualizado"})
    return jsonify(comando)

@bp.route("/upload", methods=["POST"])
def upload_arquivo():
    if "arquivo" not in request.files:
        return jsonify({"status": "erro", "mensagem": "Nenhum arquivo enviado"}), 400
    file = request.files["arquivo"]
    if file.filename == "":
        return jsonify({"status": "erro", "mensagem": "Arquivo sem nome"}), 400

    pasta = "uploads"
    os.makedirs(pasta, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = os.path.join(pasta, f"{timestamp}_{file.filename}")
    file.save(caminho)
    return jsonify({"status": "ok", "mensagem": f"Arquivo salvo como {caminho}"})

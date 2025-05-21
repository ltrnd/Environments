from flask import Blueprint, request, jsonify, send_from_directory
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
    if localizacao["latitude"] is None or localizacao["longitude"] is None:
        return jsonify({"status": "erro", "mensagem": "Nenhuma localização registrada"}), 404
    return jsonify(localizacao)

@bp.route("/comando", methods=["GET", "POST"])
def gerenciar_comando():
    global comando
    if request.method == "POST":
        data = request.get_json()
        comando["comando"] = data.get("comando")
        return jsonify({"status": "ok", "mensagem": "Comando atualizado"})
    comando_atual = comando["comando"]
    comando["comando"] = None  # limpa após pegar
    return jsonify({"comando": comando_atual})

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
    nome_arquivo = f"{timestamp}_{file.filename}"
    caminho = os.path.join(pasta, nome_arquivo)
    file.save(caminho)
    return jsonify({
        "status": "ok",
        "mensagem": f"Arquivo salvo como {caminho}",
        "url": f"/uploads/{nome_arquivo}"
    })

# ✅ ROTA: Servir arquivos da pasta uploads
@bp.route("/uploads/<path:nome_arquivo>")
def servir_arquivo(nome_arquivo):
    return send_from_directory("uploads", nome_arquivo)

# ✅ NOVA ROTA: Listar arquivos disponíveis na pasta uploads
@bp.route("/uploads", methods=["GET"])
def listar_arquivos():
    pasta = "uploads"
    if not os.path.exists(pasta):
        return jsonify({"arquivos": []})
    arquivos = os.listdir(pasta)
    arquivos.sort(reverse=True)  # Mais recentes primeiro
    return jsonify({"arquivos": arquivos})

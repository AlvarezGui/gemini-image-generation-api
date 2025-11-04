from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import *
from UserService.user_repository import (
    User, create_user, get_user_by_email, get_all_users, update_user, delete_user
)
from bson import ObjectId
import json
from AuthService.AuthController import auth_bp
from functions.generate_image import generate_image


app = Flask(__name__)
auth = HTTPBasicAuth()
users = {
    "admin": generate_password_hash("123456"),
}

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# função que verifica usuário e senha
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    # Tenta autenticar pelo MongoDB
    user = get_user_by_email(username)
    if user and check_password_hash(user.get("senha_hash"), password):
        return username
    return None

@app.route('/chat', methods=['POST'])
def process_chat():
    data = request.json
    image = generate_image(data['prompt'])
    insert_chat(data['subject'], data['user_id'], image, data['prompt'])
    return jsonify({"status": "ok", "mensagem": f"Chat salvo com sucesso!", "image_base64": image})

@app.route('/chat', methods=['DELETE'])
def chat_delete():
    data = request.json
    return delete_chat(data["chat_id"])


@app.route('/home', methods=['POST'])
def home():
    data = request.json
    home_cursor = get_home(data['user_id'])
    home_list = list(home_cursor)
    for item in home_list:
        if '_id' in item:
            item['_id'] = str(item['_id'])

    # Agora sim, retorne a lista limpa
    return jsonify({"status": "ok", "mensagem": home_list})

@app.route('/history', methods=['POST'])
def history():
    data= request.json
    history_cursor = get_history(data['user_id'])
    history_list = list(history_cursor)
    for item in history_list:
        print(item)
    return jsonify({"status": "ok", "mensagem": f"{history_list}"})

# CRUD de usuário
@app.route('/usuarios', methods=['POST'])
def api_create_user():
    dados = request.json
    user = create_user(
        dados.get("nome"),
        dados.get("email"),
        dados.get("senha")
    )
    if not user:
        return jsonify({"erro": "Email já cadastrado"}), 400
    return jsonify({"mensagem": "Usuário criado com sucesso", "usuario": user.to_dict()}), 201

@app.route('/usuarios', methods=['GET'])
def api_get_users():
    users = get_all_users()
    return jsonify(users)

@app.route('/usuarios/<email>', methods=['GET'])
def api_get_user(email):
    user = get_user_by_email(email)
    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    user.pop("senha_hash", None)
    user.pop("_id", None)
    return jsonify(user)

@app.route('/usuarios/<email>', methods=['PUT'])
def api_update_user(email):
    dados = request.json
    user = update_user(
        email,
        nome=dados.get("nome"),
        senha=dados.get("senha")
    )
    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    user.pop("senha_hash", None)
    user.pop("_id", None)
    return jsonify({"mensagem": "Usuário atualizado", "usuario": user})

@app.route('/usuarios/<email>', methods=['DELETE'])
def api_delete_user(email):
    ok = delete_user(email)
    if not ok:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    return jsonify({"mensagem": "Usuário deletado"})

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)

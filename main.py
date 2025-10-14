from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from state import salvar_prompt, ler_prompt
from UserService.user_repository import (
    User, create_user, get_user_by_email, get_all_users, update_user, delete_user
)
from AuthService.AuthController import auth_bp


app = Flask(__name__)
auth = HTTPBasicAuth()
users = {
    "admin": generate_password_hash("123456"),
}

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

@app.route('/receber_prompt', methods=['POST'])
def receber_prompt():
    dados = request.json
    # prompt_recebido = dados["prompt"]
    salvar_prompt(dados["prompt"])
    print(f"Prompt recebido do usuário {auth.current_user()}: {ler_prompt}")
    return jsonify({"status": "ok", "mensagem": f"Prompt recebido com sucesso pelo usuário {auth.current_user()}"})

# rota de teste
@app.route('/testar_rota', methods=['POST'])
def testar_rota():
    dados = request.json
    print("Foi Caralho")
    return jsonify({"status": "ok", "mensagem": f"Dados recebidos com sucesso pelo usuário {auth.current_user()}"})

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

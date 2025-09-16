from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

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
    return None

@app.route('/receber_dados', methods=['POST'])
@auth.login_required
def receber_dados():
    dados = request.json
    print(f"Dados recebidos do usuário {auth.current_user()}: {dados}")
    return jsonify({"status": "ok", "mensagem": f"Dados recebidos com sucesso pelo usuário {auth.current_user()}"})

# rota de teste
@app.route('/testar_rota', methods=['POST'])
@auth.login_required
def testar_rota():
    dados = request.json
    print("Foi Caralho")
    return jsonify({"status": "ok", "mensagem": f"Dados recebidos com sucesso pelo usuário {auth.current_user()}"})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)

from flask import Flask, request, jsonify, abort
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
from swagger.swagger_blueprint import swagger_bp
from flask_cors import CORS

SECRET_KEY = os.environ.get('API_SECRET_KEY')


app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
users = {
    "admin": generate_password_hash("123456"),
}

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.before_request
def check_api_key():
    if request.path.startswith('/swagger'):
        return
    
    if request.method == 'OPTIONS':
        return

    auth_header = request.headers.get('Authorization')

    if not auth_header or auth_header != f'Bearer {SECRET_KEY}':
        abort(403) # Proibido (Forbidden)

@app.route('/chat', methods=['POST'])
def process_chat():
    try:
        data = request.json

        required_fields = ['subject', 'user_id', 'prompt']
        if not all(field in data for field in required_fields):
            return jsonify({"status": "error", "mensagem": "Campos obrigatórios não preenchidos"}), 400

        image = generate_image(data['prompt'])
        if image == None:
            print("Erro em gerar a imagem")
            return jsonify({"status": "error", "mensagem": "Erro em gerar imagem"}), 500
        else:
            insert_chat(data['subject'], data['user_id'], image, data['prompt'])
            return jsonify({"status": "ok", "mensagem": f"Chat salvo com sucesso!", "image_base64": image}), 200
    except Exception as err:
        print(f"Erro interno : {err}")
        return jsonify({"status": "error", "mensagem": "Erro interno"}), 500

@app.route('/chat', methods=['DELETE'])
def chat_delete():
        try:
            data = request.json
            delete_chat(data["chat_id"])
            return jsonify({"status": "ok", "mensagem": "Chat deletado com sucesso!"}), 200
        except Exception as err:
            print(f"Erro ao apagar chat: {err}")
            return jsonify({"status": "error", "mensagem": "Erro interno"}), 500


@app.route('/home', methods=['POST'])
def home():
    try:
        data = request.json
        if data is None or 'user_id' not in data:
            return jsonify({"status": "error", "mensagem": "O usuário deve existir"}), 400
        else:
            home_cursor = get_home(data['user_id'])
            home_list = list(home_cursor)
            for item in home_list:
                if '_id' in item:
                    item['_id'] = str(item['_id'])
            return jsonify({"status": "ok", "mensagem": home_list}), 200
    except Exception as err:
        print(f"Erro ao buscar home: {err}")
        return jsonify({"status": "error", "mensagem": "Erro interno"}), 500

@app.route('/history', methods=['POST'])
def history():
    try:
        if request.json is None or 'user_id' not in request.json:
            return jsonify({"status": "error", "mensagem": "O usuário deve existir"}), 400
        else:
            data= request.json
            history_cursor = get_history(data['user_id'])
            history_list = list(history_cursor)
            for item in history_list:
                if '_id' in item:
                    item['_id'] = str(item['_id'])
            return jsonify({"status": "ok", "mensagem": history_list}), 200
    except Exception as err:
        print(f"Erro ao buscar histórico: {err}")
        return jsonify({"status": "error", "mensagem": "Erro interno"}), 500

# CRUD de usuário
# TODO: rotrnar o id do usuário criado
@app.route('/usuarios', methods=['POST'])
def api_create_user():
    try:
        dados = request.json
        user = create_user(
            dados.get("nome"),
            dados.get("email"),
            dados.get("senha")
        )
        if not user:
            return jsonify({"erro": "Email já cadastrado"}), 400
        return jsonify({"mensagem": "Usuário criado com sucesso", "usuario": user.to_dict()}), 201
    except Exception as err:
        print(f"Erro ao criar usuário: {err}")
        return jsonify({"erro": "Erro interno ao criar usuário"}), 500

@app.route('/usuarios', methods=['GET'])
def api_get_users():
    try:
        users = get_all_users()
        return jsonify(users)
    except Exception as err:
        print(f"Erro ao buscar usuários: {err}")
        return jsonify({"erro": "Erro interno ao buscar usuários"}), 500

@app.route('/usuarios/<email>', methods=['GET'])
def api_get_user(email):
    try:
        user = get_user_by_email(email)
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        user.pop("senha_hash", None)
        user.pop("_id", None)
        return jsonify(user)
    except Exception as err:
        print(f"Erro ao buscar usuário: {err}")
        return jsonify({"erro": "Erro interno ao buscar usuário"}), 500

@app.route('/usuarios/<email>', methods=['PUT'])
def api_update_user(email):
    try:
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
    except Exception as err:
        print(f"Erro ao atualizar usuário: {err}")
        return jsonify({"erro": "Erro interno ao atualizar usuário"}), 500

@app.route('/usuarios/<email>', methods=['DELETE'])
def api_delete_user(email):
    try:
        ok = delete_user(email)
        if not ok:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        return jsonify({"mensagem": "Usuário deletado"})
    except Exception as err:
        print(f"Erro ao deletar usuário: {err}")
        return jsonify({"erro": "Erro interno ao deletar usuário"}), 500

app.register_blueprint(auth_bp)
app.register_blueprint(swagger_bp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

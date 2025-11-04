from flask import Blueprint, request, jsonify
from UserService.user_repository import create_user, get_user_by_email, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    if not all([nome, email, senha]):
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
    if get_user_by_email(email):
        return jsonify({'erro': 'Email já cadastrado'}), 400
    user = create_user(nome, email, senha)
    if not user:
        return jsonify({'erro': 'Erro ao criar usuário'}), 500
    return jsonify({'mensagem': 'Usuário criado com sucesso', 'usuario': user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    user = get_user_by_email(email)
    if not user or not User.check_password(user.get('senha_hash'), senha):
        return jsonify({'erro': 'Credenciais inválidas'}), 401
    return jsonify({'mensagem': 'Login realizado com sucesso', 'usuario': {'nome': user.get('nome'), 'email': user.get('email')}})


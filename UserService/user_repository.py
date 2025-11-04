from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client["gemini_db"]
users_collection = db["users"]

class User:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha_hash = generate_password_hash(senha)

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "senha_hash": self.senha_hash
        }

    @staticmethod
    def check_password(senha_hash, senha):
        return check_password_hash(senha_hash, senha)

# CRUD functions

def create_user(nome, email, senha):
    if users_collection.find_one({"email": email}):
        return None  # Email já existe
    user = User(nome, email, senha)
    users_collection.insert_one(user.to_dict())
    return user

def get_user_by_email(email):
    data = users_collection.find_one({"email": email})
    return data

def get_all_users():
    return list(users_collection.find({}, {"_id": 0, "senha_hash": 0}))

def update_user(email, nome=None, senha=None):
    update_fields = {}
    if nome:
        update_fields["nome"] = nome
    if senha:
        update_fields["senha_hash"] = generate_password_hash(senha)
    if update_fields:
        users_collection.update_one({"email": email}, {"$set": update_fields})
    return get_user_by_email(email)

def delete_user(email):
    result = users_collection.delete_one({"email": email})
    return result.deleted_count > 0

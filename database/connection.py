
from pymongo.mongo_client import MongoClient
from flask import jsonify
from pymongo.server_api import ServerApi
from pymongo import MongoClient, DESCENDING
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Cluster0"] # trocar para o cluster final quando acabada a fase de testes
chats = db["chats"]
images = db["images"]
prompts = db["prompts"]

def insert_chat(subject, user_id, image, prompt):
    chat = {"subject": subject, "user_id": user_id, "image": image, "prompt": prompt}
    chats.insert_one(chat)

def delete_chat(chat_id):
    result = db.chats.delete_one({"_id": ObjectId(chat_id)})
    if result.deleted_count > 0:
        return jsonify({"status": "ok", "mensagem": "Chat deletado com sucesso"})
    else: return jsonify({"status": "erro", "mensagem": "Chat não encontrado"})

def get_home(user_id):
    return chats.find({"user_id": user_id}).sort("_id", DESCENDING).limit(10)

def get_history(user_id):
    return chats.find({"user_id": user_id}).sort("_id", DESCENDING)

# testar
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
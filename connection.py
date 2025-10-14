
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Cluster0"]
images = db["images"]
prompts = db["prompts"]

def insert_image(desc, base):
    image = {"desc": desc, "base": base}
    images.insert_one(image)

def find_image(desc):
    corresponding_images = []
    for i in images.find({}, {"desc": desc}):
        corresponding_images.append(i)
    return corresponding_images
# esta devolvendo apenas a descrição e o id
# por mais que isso seja o sufuciente, gostaria de receber o base64 na mesma chamada

# print(find_image("Imagem de teste"))

def insert_prompt(user, desc):
    prompt = {"user": user, "desc": desc}
    prompts.insert_one(prompt)

def find_prompt(user):
    result = prompts.find_one({"user": user}, {"_id": 0, "desc": 1})
    if result: return result["desc"]
    return None
    
# insert_prompt("teste2", "Games2")
# print(find_prompt("teste"))


# testar
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
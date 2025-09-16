import json
import os

FILE_PATH = "prompt.json"

def salvar_prompt(valor):
    with open(FILE_PATH, "w") as f:
        json.dump({"prompt": valor}, f)

def ler_prompt():
    if not os.path.exists(FILE_PATH):
        return None
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
        return data.get("prompt")
    
# usar o json é uma solução temporária pois claramente pode dar conflito no futuro.

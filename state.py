import json
import os
from connection import insert_prompt,find_prompt

FILE_PATH = "prompt.json"

def salvar_prompt(valor):
    # with open(FILE_PATH, "w") as f:
    #     json.dump({"prompt": valor}, f)
    insert_prompt("teste", valor)

def ler_prompt(user):
    return find_prompt(user)
    
# usar o json é uma solução temporária pois claramente pode dar conflito no futuro.

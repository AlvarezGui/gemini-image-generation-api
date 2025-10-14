from database.connection import insert_prompt,find_prompt

FILE_PATH = "prompt.json"

def salvar_prompt(user, valor):
    insert_prompt(user, valor)

def ler_prompt(user):
    return find_prompt(user)
    

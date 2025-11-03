import unittest
import sys
import os
import json
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

class UserAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_signup(self):
        email = f"{uuid.uuid4()}@teste.com"
        response = self.app.post('/signup', json={
            'nome': 'Teste',
            'email': email,
            'senha': '123456'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['mensagem'], 'Usuário criado com sucesso')

    def test_login(self):
        email = f"{uuid.uuid4()}@teste.com"
        self.app.post('/signup', json={
            'nome': 'Login',
            'email': email,
            'senha': '123456'
        })
        response = self.app.post('/login', json={
            'email': email,
            'senha': '123456'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['mensagem'], 'Login realizado com sucesso')

    def test_login_fail(self):
        response = self.app.post('/login', json={
            'email': 'naoexiste@teste.com',
            'senha': 'errada'
        })
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['erro'], 'Credenciais inválidas')

if __name__ == '__main__':
    unittest.main()

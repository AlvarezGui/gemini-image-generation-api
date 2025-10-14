
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

class UserAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_signup(self):
        response = self.app.post('/signup', json={
            'nome': 'Teste',
            'email': 'teste@teste.com',
            'senha': '123456'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Usuário criado com sucesso', response.get_data(as_text=True))

    def test_login(self):
        self.app.post('/signup', json={
            'nome': 'Login',
            'email': 'login@teste.com',
            'senha': '123456'
        })
        response = self.app.post('/login', json={
            'email': 'login@teste.com',
            'senha': '123456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login realizado com sucesso', response.get_data(as_text=True))

    def test_login_fail(self):
        response = self.app.post('/login', json={
            'email': 'naoexiste@teste.com',
            'senha': 'errada'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Credenciais inválidas', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()

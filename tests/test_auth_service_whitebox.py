import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from AuthService import AuthController

class TestAuthControllerWhiteBox(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

        self.app.add_url_rule('/signup', 'signup', AuthController.signup, methods=['POST'])
        self.app.add_url_rule('/login', 'login', AuthController.login, methods=['POST'])

    @patch("AuthService.AuthController.create_user")
    @patch("AuthService.AuthController.get_user_by_email")
    def test_signup_success(self, mock_get_user, mock_create_user):
        mock_get_user.return_value = None
        mock_create_user.return_value = MagicMock(
            to_dict=lambda: {"nome": "Teste", "email": "teste@teste.com"}
        )

        response = self.client.post('/signup', json={
            "nome": "Teste",
            "email": "teste@teste.com",
            "senha": "123456"
        })

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("Usuário criado com sucesso", data["mensagem"])

    @patch("AuthService.AuthController.get_user_by_email")
    def test_signup_email_ja_cadastrado(self, mock_get_user):
        mock_get_user.return_value = {"email": "teste@teste.com"}

        response = self.client.post('/signup', json={
            "nome": "Teste",
            "email": "teste@teste.com",
            "senha": "123"
        })

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Email já cadastrado", data["erro"])

    @patch("AuthService.AuthController.get_user_by_email")
    def test_login_fail_invalid_credentials(self, mock_get_user):
        mock_get_user.return_value = {"email": "teste@teste.com", "senha_hash": b"hash"}

        with patch("AuthService.AuthController.User.check_password", return_value=False):
            response = self.client.post('/login', json={
                "email": "teste@teste.com",
                "senha": "errada"
            })

            self.assertEqual(response.status_code, 401)
            data = response.get_json()
            self.assertIn("Credenciais inválidas", data["erro"])

    @patch("AuthService.AuthController.get_user_by_email")
    def test_login_success(self, mock_get_user):
        mock_get_user.return_value = {"nome": "Teste", "email": "teste@teste.com", "senha_hash": b"hash"}

        with patch("AuthService.AuthController.User.check_password", return_value=True):
            response = self.client.post('/login', json={
                "email": "teste@teste.com",
                "senha": "123456"
            })

            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn("Login realizado com sucesso", data["mensagem"])

"""Test authentication"""
import base64
from .base import MainTestCase


class TestAuth(MainTestCase):
    """Tests for all authentication features"""
    def test_create_account(self):
        """Test create an account"""
        res = self.client.post('/api/v2/auth/signup',
                               json=self.register_user)
        self.assertIn(b'success', res.data)
        self.assertEqual(201, res.status_code)

    def test_username_taken(self):
        """Test creating account with a taken username"""
        self.client.post('/api/v2/auth/signup',
                         json=self.register_user)
        res = self.client.post('/api/v2/auth/signup',
                               json=self.register_user)
        self.assertIn(b'The email has already been registered, use another', res.data)

    def test_wrong_credentials(self):
        res = self.client.post('/api/v2/auth/signup',
                               json={'username': '',
                                     'password': '',
                                     'email': 'johndoe@gmail.com'})
        self.assertIn(b'Enter all the required data correctly', res.data)
        res = self.client.post('/api/v2/auth/signup',
                               json={'username': '@2ndne',
                                     'password': 'Bryan12',
                                     'email': 'bryna@gmail.com'})
        self.assertIn(b'Enter only alphabetic characters for your username', res.data)

        res = self.client.post('/api/v2/auth/signup',
                               json={'username': 'Bryan',
                                     'password': 'ryan',
                                     'email': 'bryan@gmail.com'})
        self.assertIn(b'Enter a password longer than 6 characters', res.data)

        res = self.client.post('/api/v2/auth/signup',
                               json={'username': 'Bryan',
                                     'password': 'Bryan12',
                                     'email': 'bryan@gma5il.com'})
        self.assertIn(b'Enter the correct format of the email e.g. johndoe@mail.com', res.data)

        res = self.client.post('/api/v2/auth/signup',
                               json={'username': 'Bryan',
                                     'password': 'bryyane',
                                     'email': 'bryan@gmail.com'})
        self.assertIn(b'Password must have atleast one lowercase one '
                      b'upper case and one digit', res.data)

    def test_login(self):
        """Test logging in"""
        self.client.post('/api/v2/auth/signup',
                         json=self.register_user)
        user = base64.b64encode(bytes('BryanCee:Brian12', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login',
                               headers={'Authorization': 'Basic ' + user})
        self.assertIn(b'Token', res.data)

    def test_login_wrong_password(self):
        """Test logging in with wrong password"""
        self.client.post('/api/v2/auth/signup',
                         json=self.register_user)
        user = base64.b64encode(bytes('BryanCee:12345', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login',
                               headers={'Authorization': 'Basic ' + user})
        self.assertIn(b'Could not verify, invalid credentials check your username or password', res.data)

    def test_login_user_not_exist(self):
        user = base64.b64encode(bytes('BryanCee:123456', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login',
                               headers={'Authorization': 'Basic ' + user})
        self.assertIn(b'Could not verify, invalid credentials check your username or password', res.data)

    def test_login_wrong_authorization_info(self):
        self.client.post('/api/v2/auth/signup',
                         json=self.register_user)
        user = base64.b64encode(bytes('BryanCee:', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})
        self.assertIn(b'Could not verify, please input all your credentials', res.data)

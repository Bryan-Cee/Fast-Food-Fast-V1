"""Test authentication"""
import base64
from .base import MainTestCase


class TestAuth(MainTestCase):
    """Tests for all authentication features"""
    def test_create_account(self):
        """Test create an account"""
        res = self.client.post('/api/v2/auth/signup',
                               json={'username': 'JohnDoe',
                                     'password': 'JohnDoe12'})
        self.assertIn(b'Success', res.data)
        self.assertEqual(201, res.status_code)

    def test_username_taken(self):
        """Test creating account with a taken username"""
        self.client.post('/api/v2/auth/signup',
                         json={'username': 'JohnDoe',
                               'password': 'JohnDoe12'})
        res = self.client.post('/api/v2/auth/signup',
                               json={'username': 'JohnDoe',
                                     'password': 'JohnDoe12'})
        self.assertEqual(b'The username has already been taken please try another', res.data)

    def test_wrong_credentials(self):
        res = self.client.post('/api/v2/auth/signup',
                               json={'username': '',
                                     'password': ''})
        self.assertEqual(b'Invalid entry: please enter the correct '
                         b'JSON format - "username":"your_username"'
                         b', "password":"your_password"', res.data)
        res = self.client.post('/api/v2/auth/signup',
                               json={'username': '@2ndne',
                                     'password': 'Bryan12'})
        self.assertEqual(b'Enter only alphabetic characters for your username', res.data)

        res = self.client.post('/api/v2/auth/signup',
                               json={'username': 'Bryan',
                                     'password': 'ryan'})
        self.assertEqual(b'Enter a password longer than 6 characters', res.data)

        res = self.client.post('/api/v2/auth/signup',
                               json={'username': 'Bryan',
                                     'password': 'bryyane'})
        self.assertEqual(b'Password must have atleast one lowercase one '
                         b'upper case and one digit', res.data)

    def test_login(self):
        """Test logging in"""
        self.client.post('/api/v2/auth/signup',
                         json={'username': 'BryanCee',
                               'password': 'Brian12'})
        user = base64.b64encode(bytes('BryanCee:Brian12', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login',
                               headers={'Authorization': 'Basic ' + user})
        self.assertIn(b'Token', res.data)

    def test_login_wrong_password(self):
        """Test logging in with wrong password"""
        self.client.post('/api/v2/auth/signup',
                         json={'username': 'BryanCee',
                               'password': 'Brian12'})
        user = base64.b64encode(bytes('BryanCee:12345', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login',
                               headers={'Authorization': 'Basic ' + user})
        self.assertIn(b'wrong password', res.data)

    def test_login_user_not_exist(self):
        user = base64.b64encode(bytes('BryanCee:123456', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login',
                               headers={'Authorization': 'Basic ' + user})
        self.assertIn(b'Could not verify, user is not registred', res.data)

    def test_login_wrong_authorization_info(self):
        self.client.post('/api/v2/auth/signup',
                         json={'username': 'BryanCee',
                               'password': '123456'})
        user = base64.b64encode(bytes('BryanCee:', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})
        self.assertEqual(b'Could not verify, please input all your credentials', res.data)

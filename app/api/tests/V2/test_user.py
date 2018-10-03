"""Tests for user"""
import datetime

import ast
import base64
import jwt

from .base import MainTestCase


class TestUser(MainTestCase):
    """Test cases for user functionality"""
    def test_make_order_not_authenticated(self):
        """Test making an order when not authenticated"""
        res = self.client.post('/api/v2/users/orders', json={'meal_id': 1})
        self.assertEqual('Token is missing', res.get_data(as_text=True))

    def test_make_valid_order(self):
        """"Test making an order"""
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + self.user})
        # Admin creates a meal in the menu
        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        self.client.post('/api/v2/menu',
                         headers={'x-access-token': final_token},
                         json=self.correct_order)

        # User creates an account
        self.client.post('/api/v2/auth/signup', json={'username': 'Bellacee',
                                                      'password': 'Bella12',
                                                      'email': 'johndoe@gmail.com'})
        # User logs in to the account
        user = base64.b64encode(bytes('Bellacee:Bella12', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})
        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        # User creates an order
        res = self.client.post('/api/v2/users/orders',
                               headers={'x-access-token': final_token},
                               json={"meal_id": 1})
        self.assertIn('Order has been received', res.get_data(as_text=True))
        no_id_res = self.client.post('/api/v2/users/orders',
                                     headers={'x-access-token': final_token},
                                     json={})
        self.assertEqual('Please enter the correct JSON format: "meal_id":id, "quantity":number"',
                         no_id_res.get_data(as_text=True))

    def test_get_user_history(self):
        """Test getting user history"""
        self.client.post('/api/v2/auth/signup', json={'username': 'Bellacee',
                                                      'password': 'Bella12',
                                                      'email': 'bellacee@gmail.com'})
        # User logs in to the account
        user = base64.b64encode(bytes('Bellacee:Bella12', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})
        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        res = self.client.get('/api/v2/users/orders',
                              headers={'x-access-token': final_token})
        self.assertIn('You have no history', res.get_data(as_text=True))

    def test_get_user_history_ordered(self):
        """Test getting user history"""
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' +self. user})
        # Admin creates a meal in the menu
        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        self.client.post('/api/v2/menu',
                         headers={'x-access-token': final_token},
                         json=self.correct_order)
        # User create account
        self.client.post('/api/v2/auth/signup', json={'username': 'Bellacee',
                                                      'password': 'Bella12',
                                                      'email': 'johndoe@gmail.com'})
        # User logs in to the account
        user = base64.b64encode(bytes('Bellacee:Bella12', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})
        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        # User makes an order
        self.client.post('/api/v2/users/orders',
                         headers={'x-access-token': final_token},
                         json={"meal_id": 1})
        res = self.client.get('/api/v2/users/orders',
                              headers={'x-access-token': final_token})
        self.assertIn(b'User_History', res.get_data())
        # User makes an invalid order
        res = self.client.post('/api/v2/users/orders',
                               headers={'x-access-token': final_token},
                               json={"meal_id": 254})
        self.assertIn(b'The meal does not exists in the menu', res.get_data())

    def test_view_history_without_login(self):
        """Test viewing history without logging in"""
        token = jwt.encode({'user_id': 2,
                            'iat': datetime.datetime.now(),
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
                           "secret",
                           algorithm='HS256')

        res = self.client.get('/api/v2/users/orders',
                              headers={'x-access-token': token})
        self.assertEqual("Login to view order history", res.get_data(as_text=True))

    def test_order_meal_without_login(self):
        """Test ordering meals without logging in"""
        token = jwt.encode({'user_id': 2,
                            'iat': datetime.datetime.now(),
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
                           "secret",
                           algorithm='HS256')

        res = self.client.post('/api/v2/users/orders',
                               headers={'x-access-token': token})
        self.assertEqual("Please login to order", res.get_data(as_text=True))

    def test_token_expired(self):
        """Test using an expired auth - token"""
        token = jwt.encode({'user_id': 1,
                            'iat': datetime.datetime.now(),
                            'exp': datetime.datetime.utcnow() - datetime.timedelta(minutes=5)},
                           "secret",
                           algorithm='HS256')

        res = self.client.get('/api/v2/users/orders',
                              headers={'x-access-token': token})
        self.assertEqual("Token has expired Please login again", res.get_data(as_text=True))

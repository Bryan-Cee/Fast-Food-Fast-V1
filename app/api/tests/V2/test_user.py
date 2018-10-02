import datetime

from .base import MainTestCase
import ast
import base64
import jwt


class TestUser(MainTestCase):

    def test_make_order_not_authenticated(self):
        res = self.client.post('/api/v2/users/orders', json={'meal_id': 1})
        self.assertEqual('Token is missing', res.get_data(as_text=True))

    def test_make_valid_order(self):
        # Create an admin account
        self.client.post('/api/v2/auth/signup', json={'username': 'BryanCee',
                                                      'password': '123456',
                                                      'Admin': 'True'})
        # Admin login
        user = base64.b64encode(bytes('BryanCee:123456', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})
        # Admin creates a meal in the menu
        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        self.client.post('/api/v2/menu',
                         headers={'x-access-token': final_token},
                         json={"meal_name": 'Pizza',
                               "meal_desc": 'Seasoned',
                               "meal_price": 7.99})

        # User creates an account
        self.client.post('/api/v2/auth/signup', json={'username': 'Bellacee',
                                                      'password': '123456'})
        # User logs in to the account
        user = base64.b64encode(bytes('Bellacee:123456', 'UTF-8')).decode('UTF-8')
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
        self.assertEqual('Please enter the correct format of keys', no_id_res.get_data(as_text=True))

    def test_get_user_history(self):
        self.client.post('/api/v2/auth/signup', json={'username': 'Bellacee',
                                                      'password': '123456'})
        # User logs in to the account
        user = base64.b64encode(bytes('Bellacee:123456', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})
        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        res = self.client.get('/api/v2/users/orders',
                              headers={'x-access-token': final_token})
        self.assertIn('You have no history', res.get_data(as_text=True))

    def test_get_user_history_ordered(self):
        # Create an admin account
        self.client.post('/api/v2/auth/signup', json={'username': 'BryanCee',
                                                      'password': '123456',
                                                      'Admin': 'True'})
        # Admin login
        user = base64.b64encode(bytes('BryanCee:123456', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})
        # Admin creates a meal in the menu
        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        self.client.post('/api/v2/menu',
                         headers={'x-access-token': final_token},
                         json={"meal_name": 'Pizza',
                               "meal_desc": 'Seasoned',
                               "meal_price": 7.99})
        # User create account
        self.client.post('/api/v2/auth/signup', json={'username': 'Bellacee',
                                                      'password': '123456'})
        # User logs in to the account
        user = base64.b64encode(bytes('Bellacee:123456', 'UTF-8')).decode('UTF-8')
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
        token = jwt.encode({'user_id': 1,
                            'iat': datetime.datetime.now(),
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
                           "secret_to_encoding",
                           algorithm='HS256')

        res = self.client.get('/api/v2/users/orders',
                              headers={'x-access-token': token})
        self.assertEqual("Login to view order history", res.get_data(as_text=True))

    def test_order_meal_without_login(self):
        token = jwt.encode({'user_id': 1,
                            'iat': datetime.datetime.now(),
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
                           "secret_to_encoding",
                           algorithm='HS256')

        res = self.client.post('/api/v2/users/orders',
                               headers={'x-access-token': token})
        self.assertEqual("Please login to order", res.get_data(as_text=True))

    def test_token_expired(self):
        token = jwt.encode({'user_id': 1,
                            'iat': datetime.datetime.now(),
                            'exp': datetime.datetime.utcnow() - datetime.timedelta(minutes=5)},
                           "secret_to_encoding",
                           algorithm='HS256')

        res = self.client.get('/api/v2/users/orders',
                              headers={'x-access-token': token})
        self.assertEqual("Token has expired Please login again", res.get_data(as_text=True))


import base64
import ast

from .base import MainTestCase


class TestAddMealToMenu(MainTestCase):

    def test_add_meal_token_missing(self):
        res = self.client.post('/api/v2/menu', json={"meal_name": 'Pizza',
                                                     "meal_desc": 'Seasoned',
                                                     "meal_price": 7.99})
        self.assertEqual('Token is missing', res.get_data(as_text=True))

    def test_add_meal_admin(self):
        self.client.post('/api/v2/auth/signup', json={'username': 'BryanCee',
                                                      'password': '123456',
                                                      'Admin': 'True'})
        self.client.post('/api/v2/auth/login', json={'username': 'BryanCee',
                                                     'password': '123456'})

        user = base64.b64encode(bytes('BryanCee:123456', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})

        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        res = self.client.post('/api/v2/menu',
                               headers={'x-access-token': final_token},
                               json={"meal_name": 'Pizza',
                                     "meal_desc": 'Seasoned',
                                     "meal_price": 7.99})
        self.assertIn('Meal has been added to the menu', res.get_data(as_text=True))

    def test_add_meal_twice(self):
        self.client.post('/api/v2/auth/signup', json={'username': 'BryanCee',
                                                      'password': '123456',
                                                      'Admin': 'True'})
        self.client.post('/api/v2/auth/login', json={'username': 'BryanCee',
                                                     'password': '123456'})

        user = base64.b64encode(bytes('BryanCee:123456', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})

        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        self.client.post('/api/v2/menu',
                         headers={'x-access-token': final_token},
                         json={"meal_name": 'Pizza',
                               "meal_desc": 'Seasoned',
                               "meal_price": 7.99})
        res = self.client.post('/api/v2/menu',
                               headers={'x-access-token': final_token},
                               json={"meal_name": 'Pizza',
                                     "meal_desc": 'Seasoned',
                                     "meal_price": 7.99})
        self.assertIn('The meal is already in the menu', res.get_data(as_text=True))

    def test_add_meal_wrong_data(self):
        self.client.post('/api/v2/auth/signup', json={'username': 'BryanCee',
                                                      'password': '123456',
                                                      'Admin': 'True'})
        self.client.post('/api/v2/auth/login', json={'username': 'BryanCee',
                                                     'password': '123456'})

        user = base64.b64encode(bytes('BryanCee:123456', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})

        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        res = self.client.post('/api/v2/menu',
                               headers={'x-access-token': final_token},
                               json={"meal_desc": 'Seasoned',
                                     "meal_price": 7.99})
        self.assertIn('Please enter the correct format of keys', res.get_data(as_text=True))

    def test_add_meal_non_admin(self):
        self.client.post('/api/v2/auth/signup', json={'username': 'BryanCee',
                                                      'password': '123456'})
        self.client.post('/api/v2/auth/login', json={'username': 'BryanCee',
                                                     'password': '123456'})

        user = base64.b64encode(bytes('BryanCee:123456', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})

        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        res = self.client.post('/api/v2/menu',
                               headers={'x-access-token': final_token},
                               json={"meal_name": 'Pizza',
                                     "meal_desc": 'Seasoned',
                                     "meal_price": 7.99})
        self.assertIn('You are not an administrator', res.get_data(as_text=True))

    def test_get_menu(self):
        self.client.post('/api/v2/auth/signup', json={'username': 'BryanCee',
                                                      'password': '123456',
                                                      'Admin': 'True'})
        self.client.post('/api/v2/auth/login', json={'username': 'BryanCee',
                                                     'password': '123456'})

        user = base64.b64encode(bytes('BryanCee:123456', 'UTF-8')).decode('UTF-8')
        res = self.client.post('/api/v2/auth/login', headers={'Authorization': 'Basic ' + user})

        token = res.get_data(as_text=True)
        final_token = ast.literal_eval(token.replace(" ", ""))['Token']
        res = self.client.get('/api/v2/menu', headers={"x-access-token": final_token})
        self.assertIn('There is no meal in the menu at the moment', res.get_data(as_text=True))
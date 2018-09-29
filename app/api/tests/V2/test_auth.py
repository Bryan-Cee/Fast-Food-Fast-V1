import base64
from .base import MainTestCase
from werkzeug.datastructures import Headers


class TestAuth(MainTestCase):

	def test_create_account(self):
		res = self.client.post('/api/v2/auth/signup', json={'username': 'John Doe', 'password': '123456'})
		self.assertIn(b'Success', res.data)
		self.assertEqual(201, res.status_code)

	def test_username_taken(self):
		self.client.post('/api/v2/auth/signup', json={'username': 'John Doe', 'password': '123456'})
		res = self.client.post('/api/v2/auth/signup', json={'username': 'John Doe', 'password': '123456'})
		self.assertEqual(b'The username has already been taken please try another', res.data)

	def test_no_username_or_password(self):
		res = self.client.post('/api/v2/auth/signup', json={'username': '', 'password': ''})
		self.assertEqual(b'Invalid, no user name or password', res.data)

	def test_login_wrong_password(self):
		self.client.post('/api/v2/auth/signup', json={'username': 'BryanCee', 'password': '123456'})
		h = Headers()
		user = base64.b64encode(bytes('BryanCee:12345', 'UTF-8')).decode('UTF-8')
		h.add('Authorization', 'Basic ' + user)
		res = self.client.post('/api/v2/auth/login', headers=h)
		self.assertEqual(b'wrong password', res.data)

	def test_login_no_authorization(self):
		self.client.post('/api/v2/auth/signup', json={'username': 'BryanCee', 'password': '123456'})
		h = Headers()
		user = base64.b64encode(bytes('BryanCee:', 'UTF-8')).decode('UTF-8')
		h.add('Authorization', 'Basic ' + user)
		res = self.client.post('/api/v2/auth/login', headers=h)
		self.assertEqual(b'Could not verify, please input all your credentials', res.data)

	def test_no_user(self):
		h = Headers()
		user = base64.b64encode(bytes('BryanCee:123456', 'UTF-8')).decode('UTF-8')
		h.add('Authorization', 'Basic ' + user)
		res = self.client.post('/api/v2/auth/login', headers=h)
		self.assertEqual(b'Could not verify, please check your username or password', res.data)

	def test_login(self):
		self.client.post('/api/v2/auth/signup', json={'username': 'BryanCee', 'password': '123456'})
		h = Headers()
		user = base64.b64encode(bytes('BryanCee:123456', 'UTF-8')).decode('UTF-8')
		h.add('Authorization', 'Basic ' + user)
		res = self.client.post('/api/v2/auth/login', headers=h)
		self.assertIn(b'Token', res.data)

from .base import MainTestCase


class TestAuth(MainTestCase):

	def test_create_account(self):
		res = self.client.post('/api/v2/auth/sigup', json={'username': 'John Doe', 'password': '123456'})
		self.assertIn('Success', res.data)
		self.assertEqual(201, res.status_code)
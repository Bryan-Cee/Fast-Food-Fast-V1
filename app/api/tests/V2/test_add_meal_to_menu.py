from .base import MainTestCase


class TestAddMealToMenu(MainTestCase):

	def test_add_meal(self):
		res = self.client.post('/api/v2/menu', json={"meal_name": 'Pizza', "meal_desc": 'Seasoned', "meal_price": 7.99})
		self.assertIn('Meal has been added to the menu', res.get_data(as_text=True))
		self.assertEqual(201, res.status_code)

		res = self.client.post('/api/v2/menu', json={})
		self.assertEqual(b'Please enter the correct format of keys', res.data)

		res = self.client.post('/api/v2/menu', json={"meal_name": 'Pizza', "meal_desc": 'Seasoned', "meal_price": 7.99})
		self.assertEqual(b'The meal is already in the menu', res.data)

	def test_get_menu(self):
		res = self.client.get('/api/v2/menu')
		self.assertEqual(200, res.status_code)


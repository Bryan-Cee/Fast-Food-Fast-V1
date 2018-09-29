from .base import MainTestCase


class TestAddMealToMenu(MainTestCase):

	def test_add_meal(self):
		res = self.client.post('/api/v2/menu', json={"meal_name": 'Pizza', "meal_desc": 'Seasoned', "meal_price": 7.99})
		self.assertEqual('{"status": "Meal has been added to the menu"}', res.data)
		self.assertEqual(201, res.status_code)

		res = self.client.post('/api/v2/menu')
		self.assertEqual('Please enter the correct format of keys', res.data)

		res = self.client.post('/api/v2/menu', json={"meal_name": 'Pizza', "meal_desc": 'Seasoned', "meal_price": 7.99})
		self.assertEqual('The meal is already in the menu', res.data)

	def test_get_menu(self):
		res = self.client.get('/api/v2/menu')
		self.assertEqual(200, res.status_code)


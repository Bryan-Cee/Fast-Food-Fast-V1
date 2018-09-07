from unittest import TestCase


class TestEndpoints(TestCase):

	def setUp(self):
		from app import create_app
		self.app = create_app()
		self.client = self.app.test_client()
		self.app_context = self.app.app_context()

	def test_get_all_orders_when_none_exist(self):
		res = self.client.get("/api/V1/orders")
		self.assertEqual(res.status_code, 200)
		self.assertEqual('No orders yet', res.get_data(as_text=True))

	def test_get_menu_with_no_meals(self):
		res = self.client.get("/api/V1/menu")
		self.assertEqual(200, res.status_code)
		self.assertEqual('No meals have been added to the menu', res.get_data(as_text=True))

	def test_adding_meal_to_menu(self):
		res = self.client.post("/api/V1/menu", json={'foodname': 'Pizza', 'price': '$4.99'})
		self.assertEqual(201, res.status_code)
		self.assertEqual('Meal added', res.get_data(as_text=True))
		print(res.get_data(as_text=True))

	def test_get_menu_with_meals(self):
		res = self.client.post("/api/V1/menu", json={'foodname': 'Pizza', 'price': '$4.99'})
		self.assertEqual(201, res.status_code)
		res = self.client.get("/api/V1/menu")
		self.assertEqual(200, res.status_code)

	def test_get_all_order_when_orders_exist(self):
		res = self.client.post("/api/V1/menu", json={'foodname': 'Pizza', 'price': '$4.99'})
		self.assertEqual(201, res.status_code)
		res = self.client.get("/api/V1/orders")
		self.assertEqual(200, res.status_code)


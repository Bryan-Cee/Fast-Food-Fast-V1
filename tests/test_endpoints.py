import unittest


class TestEndpoints(unittest.TestCase):

    def setUp(self):
        from app import create_app
        self.app = create_app()
        self.client = self.app.test_client()

    def test_entry(self):
        res = self.client.get("/")
        self.assertEqual(200, res.status_code)

    def test_get_all_orders(self):
        res = self.client.get("/api/V1/orders")
        self.assertEqual(res.status_code, 200)
        self.assertEqual('No orders yet', res.get_data(as_text=True))

        with self.app.test_request_context():
            self.client.post(
                "/api/V1/menu", json={'foodname': 'Pizza', 'price': '$4.99'})
            self.client.post("/api/V1/orders",
                             json={'foodname': 'Pizza', 'price': '$6.99'})
            res = self.client.get("/api/V1/orders")
            self.assertIn("Pizza", res.get_data(as_text=True))

    def test_get_specific_order(self):
        with self.app.test_request_context():
            self.client.post(
                "/api/V1/menu", json={'foodname': 'Pizza', 'price': '$4.99'})
            self.client.post("/api/V1/orders",
                             json={'foodname': 'Pizza', 'price': '$6.99'})
            res = self.client.get("/api/V1/orders/1")
            self.assertIn("Pizza", res.get_data(as_text=True))

            res = self.client.get("/api/V1/orders/0")
            self.assertEqual("The order was not found",
                             res.get_data(as_text=True))

    def test_modifying_status(self):
        with self.app.test_request_context():
            self.client.post(
                "/api/V1/menu", json={'foodname': 'Pizza', 'price': '$4.99'})
            self.client.post("/api/V1/orders",
                             json={'foodname': 'Pizza', 'price': '$6.99'})
            self.client.put("/api/V1/orders/1", json={'status': 'accepted'})
            res = self.client.get("/api/V1/orders/1")
            self.assertIn("accepted", res.get_data(as_text=True))

            res = self.client.put("/api/V1/orders/0",
                                  json={'status': 'accepted'})
            self.assertEqual("The order was not found",
                             res.get_data(as_text=True))

    def test_adding_meal_to_menu(self):
        res = self.client.post(
            "/api/V1/menu", json={'foodname': 'Pizza', 'price': '$4.99'})
        self.assertEqual(201, res.status_code)
        self.assertEqual('Meal added', res.get_data(as_text=True))

        with self.app.test_request_context():
            self.client.post(
                "/api/V1/menu", json={'foodname': 'Pizza', 'price': '$4.99'})
            res = self.client.get("/api/V1/menu")
            order = res.get_json()
            for item in order.values():
                orders = item
            assert orders[0]['order_id'] == 1

            self.client.post(
                "/api/V1/menu", json={'foodname': 'Burger', 'price': '$4.99'})
            res = self.client.get("/api/V1/menu")
            order = res.get_json()
            for item in order.values():
                orders = item
            assert orders[1]['order_id'] == 2

            res = self.client.post(
                "/api/V1/menu", json={'foodname': 'Burger', 'price': '$4.99'})
            self.assertEqual('Meal is already in the menu',
                             res.get_data(as_text=True))

    def test_get_menu(self):
        res = self.client.get("/api/V1/menu")
        self.assertEqual(200, res.status_code)
        self.assertEqual('No meals have been added to the menu',
                         res.get_data(as_text=True))

        res = self.client.post(
            "/api/V1/menu", json={'foodname': 'Pizza', 'price': '$4.99'})
        self.assertEqual(201, res.status_code)
        res = self.client.get("/api/V1/menu")
        self.assertEqual(200, res.status_code)

    def test_for_order(self):
        with self.app.test_request_context():
            self.client.post(
                "/api/V1/menu", json={'foodname': 'Pizza', 'price': '$4.99'})
            self.client.post(
                "/api/V1/menu", json={'foodname': 'Burger', 'price': '$7.99'})

            self.client.post("/api/V1/orders", json={'foodname': 'Pizza'})
            res = self.client.get("/api/V1/orders")
            order = res.get_json()
            for item in order.values():
                orders = item
            assert orders[0]['order_id'] == 1

            self.client.post("/api/V1/orders", json={'foodname': 'Burger'})
            res = self.client.get("/api/V1/menu")
            order = res.get_json()
            for item in order.values():
                orders = item
            assert orders[1]['order_id'] == 2

            res = self.client.post(
                "/api/V1/orders", json={'foodname': 'Hot dog'})
            self.assertEqual(
                "Invalid order, the food you ordered is not in the menu", res.get_data(as_text=True))

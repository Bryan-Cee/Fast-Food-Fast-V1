""""app/api/tests/v2/base.py"""
import base64
import os
import unittest
import psycopg2
from app.database import Default
from app import create_app

connector = os.getenv('DATABASE_URL')


class MainTestCase(unittest.TestCase):
    """Set up for test"""
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.correct_order = {"meal_name": 'Pizza',
                              "meal_desc": 'Seasoned',
                              "meal_price": 7.99}
        self.register_user = {'username': 'BryanCee',
                              'password': 'Brian12',
                              'email': 'bryancee@gmail.com'}
        self.user = base64.b64encode(bytes('Admin:Admin12', 'UTF-8')).decode('UTF-8')

    def tearDown(self):
        conn = psycopg2.connect(connector)

        with conn:
            with conn.cursor() as cur:
                commands = Default().drop
                for command in commands:
                    cur.execute(command)
        conn.close()
        self.app_context.pop()

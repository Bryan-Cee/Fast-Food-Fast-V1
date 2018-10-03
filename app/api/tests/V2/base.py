""""app/api/tests/v2/base.py"""
import unittest
import psycopg2
from instance.config import TestingConfig
from app.api.v2.database import Default
from app import create_app

DBNAME = TestingConfig.DBNAME
USER = TestingConfig.USER
PASSWORD = TestingConfig.USER


class MainTestCase(unittest.TestCase):
    """Set up for test"""
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        conn = psycopg2.connect(host='localhost', database=DBNAME, user=USER, password=PASSWORD)

        with conn:
            with conn.cursor() as cur:
                commands = Default().drop
                for command in commands:
                    cur.execute(command)
        conn.close()
        self.app_context.pop()

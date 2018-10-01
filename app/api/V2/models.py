import psycopg2
import os
from .database import Default

conn = psycopg2.connect(dbname=os.getenv('database'),

                        user=os.getenv('user'),

                        password=os.getenv('password'))

cur = conn.cursor()

create_tables = Default().commands

for command in create_tables:
    cur.execute(command)

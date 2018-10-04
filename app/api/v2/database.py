import os
import psycopg2
from werkzeug.security import generate_password_hash

from instance.config import app_configs

config = app_configs[os.getenv('APP_SETTINGS')]


class Default:
    """Initialize the tables in the database"""
    commands = (
        """	
        CREATE TABLE IF NOT EXISTS Users (
            user_id serial NOT NULL PRIMARY KEY,
            username varchar(45) NOT NULL,
            email varchar(100) NOT NULL,
            password varchar(255) NOT NULL,
            Admin boolean DEFAULT False  NOT NULL
            );
        """
        ,
        """
        CREATE TABLE IF NOT EXISTS Menu (
            meal_id serial PRIMARY KEY NOT NULL,
            meal_name varchar(45) NOT NULL,
            meal_desc varchar(100),
            meal_price float NOT NULL
        );
        
        """
        ,
        """
        CREATE TABLE IF NOT EXISTS  Orders (
            order_id serial NOT NULL PRIMARY KEY,
            meal_id int NOT NULL,
            time_of_order timestamp NOT NULL,
            user_id int NOT NULL,
            order_status varchar(20) DEFAULT 'new' NOT NULL,
            quantity int NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (meal_id) REFERENCES Menu (meal_id) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """
    )

    drop = (
        """
        DROP TABLE IF EXISTS Users CASCADE;
        """
        ,
        """
        DROP TABLE IF EXISTS Orders CASCADE;
        """
        ,
        """
        DROP TABLE IF EXISTS Menu CASCADE;
        """

    )


class InitDB:
    def __init__(self, configs):
        self.conn = psycopg2.connect(config.DATABASE_URL)

    def create_tables(self):
        password = os.getenv('ADMIN_PASSWORD')
        email = os.getenv('ADMIN_EMAIL')
        username = os.getenv('ADMIN_NAME')

        hashed_pwd = generate_password_hash(password, method='sha256')
        conn = self.conn
        with conn:
            with conn.cursor() as cur:
                create_tables = Default().commands
                for command in create_tables:
                    cur.execute(command)
                cur.execute("INSERT INTO Users(username, email, password, admin) "
                            "VALUES (%s, %s, %s, TRUE)", (username, email, hashed_pwd))
                conn.commit()
        conn.close()

import psycopg2


class Default:
    """Initialize the tables in the database"""
    commands = (
        """	
        DROP TABLE IF EXISTS Users CASCADE;
        CREATE TABLE IF NOT EXISTS Users (
            user_id serial NOT NULL PRIMARY KEY,
            username varchar(45) NOT NULL,
            password varchar(255) NOT NULL,
            Admin boolean DEFAULT False  NOT NULL
            );
        """
        ,
        """
        DROP TABLE IF EXISTS Orders CASCADE;
        CREATE TABLE IF NOT EXISTS  Orders (
            order_id serial NOT NULL PRIMARY KEY,
            meal_id int NOT NULL,
            time_of_order time NOT NULL,
            user_id int NOT NULL,
            order_status varchar(20) DEFAULT 'new order' NOT NULL
        );
        """
        ,
        """
        DROP TABLE IF EXISTS Menu CASCADE;
        CREATE TABLE IF NOT EXISTS Menu (
            meal_id serial PRIMARY KEY NOT NULL,
            meal_name varchar(45) NOT NULL,
            meal_desc varchar(100),
            meal_price float NOT NULL
        );
        """
        ,
        """
        ALTER TABLE Orders
        ADD CONSTRAINT orders_users_user_id_fk
        FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE ON UPDATE CASCADE;
        """
        ,
        """
        ALTER TABLE Orders
        ADD CONSTRAINT orders_menu_meal_id_fk
        FOREIGN KEY (meal_id) REFERENCES Menu (meal_id) ON DELETE CASCADE ON UPDATE CASCADE;
        """
    )


class TestDatabase:
    """Initializes the tables in the test database"""

    sql = (
        """	
        DROP TABLE IF EXISTS Users CASCADE;
        CREATE TABLE IF NOT EXISTS Users (
            user_id serial NOT NULL PRIMARY KEY,
            username varchar(45) NOT NULL,
            password varchar(255) NOT NULL,
            Admin boolean DEFAULT FALSE  NOT NULL
            );
        """
        ,
        """
        DROP TABLE IF EXISTS Orders CASCADE;
        CREATE TABLE IF NOT EXISTS  Orders (
            order_id serial NOT NULL PRIMARY KEY,
            meal_id int NOT NULL,
            time_of_order time NOT NULL,
            user_id int NOT NULL
        );
        """
        ,
        """
        DROP TABLE IF EXISTS Menu CASCADE;
        CREATE TABLE IF NOT EXISTS Menu (
            meal_id serial PRIMARY KEY NOT NULL,
            meal_name varchar(45) NOT NULL,
            meal_desc varchar(100)
        );
        """
        ,
        """
        ALTER TABLE Orders
        ADD CONSTRAINT orders_users_user_id_fk
        FOREIGN KEY (order_id) REFERENCES Users (user_id) ON DELETE CASCADE ON UPDATE CASCADE;
        """
        ,
        """
        ALTER TABLE Orders
        ADD CONSTRAINT orders_menu_meal_id_fk
        FOREIGN KEY (meal_id) REFERENCES Menu (meal_id) ON DELETE CASCADE ON UPDATE CASCADE;
        """
    )


class InitDB:
    def __init__(self, config):
        self.dbame = config.get('DBNAME')
        self.user = config.get('USER')
        self.password = config.get('PASSWORD')

    def create_tables(self):
        conn = psycopg2.connect(host="localhost",
                                database=self.dbame,
                                user=self.user,
                                password=self.password)
        cur = conn.cursor()
        create_tables = Default().commands
        for command in create_tables:
            cur.execute(command)
        conn.commit()
        cur.close()
        conn.close()

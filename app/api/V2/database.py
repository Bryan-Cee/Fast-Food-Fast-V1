class Default:
	"""Initialize the tables in the database"""
	commands = (
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
			time_of_oder time NOT NULL,
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
		ADD CONSTRAINT orders_users_user_id_fk
		FOREIGN KEY (order_id) REFERENCES Users (user_id) ON DELETE CASCADE ON UPDATE CASCADE;
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
			time_of_oder time NOT NULL,
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
		ADD CONSTRAINT orders_users_user_id_fk
		FOREIGN KEY (order_id) REFERENCES Users (user_id) ON DELETE CASCADE ON UPDATE CASCADE;
		"""
	)
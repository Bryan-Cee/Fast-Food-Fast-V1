import psycopg2
import app.config as config


conn = psycopg2.connect(host="localhost",
                        database=config.DBNAME,
                        user=config.USER,
                        password=config.PASSWORD)


def place_order(meal_id, user_id, time):
    with conn:
        with conn.cursor() as cur:
            if not meal_id or not user_id:
                conn.rollback()
                return 'Please enter the correct format of keys'
            try:
                cur.execute("INSERT INTO Orders(meal_id, user_id, time_of_order) VALUES (%s, %s, %s)",
                            (meal_id, user_id, time))
            except psycopg2.IntegrityError:
                return "The meal does not exists in the menu"
            finally:
                conn.commit()
    return "Order has been received"

import psycopg2
from datetime import datetime
from config.config import HOST, PORT, DBNAME, PASSWORD, USER


class PgConn:
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(database=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
            self.cur = self.conn.cursor()

        except(Exception, psycopg2.DatabaseError, psycopg2.OperationalError) as error:
            print(error)

    def create_tables(self):
        with self.conn:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS Users(
                                    id SERIAL PRIMARY KEY NOT NULL,
                                    id_tg BIGINT ,
                                    username CHARACTER VARYING(100) ,
                                    name CHARACTER VARYING(60),
                                    surname CHARACTER VARYING(60),
                                    date_reg TIMESTAMP WITHOUT TIME ZONE,
                                    phone_numb CHARACTER VARYING(15)) """)
            self.conn.commit()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS Users_Information(
                                    user_id INTEGER REFERENCES Users(id) ON DELETE SET NULL,
                                    latitude CHARACTER VARYING(30),
                                    longitude CHARACTER VARYING(30),
                                    is_admin BOOLEAN DEFAULT FALSE,
                                    last_chosen_category_id INTEGER,
                                    last_chosen_product_id INTEGER,
                                    last_chosen_quantity INTEGER,
                                    temp CHARACTER VARYING(50) DEFAULT 'no',
                                    lang CHARACTER VARYING(2) DEFAULT 'ru')""")

            self.cur.execute(""" CREATE TABLE IF NOT EXISTS Categories(
                                    id SERIAL PRIMARY KEY NOT NULL,
                                    name_uz CHARACTER VARYING(200) UNIQUE NOT NULL ,
                                    name_ru CHARACTER VARYING(200) UNIQUE NOT NULL ,
                                    name_en CHARACTER VARYING(200) UNIQUE NOT NULL ,
                                    is_deleted BOOLEAN DEFAULT FALSE
                                )
            """)

            self.cur.execute("""CREATE TABLE IF NOT EXISTS Products(
                                    id SERIAL PRIMARY KEY NOT NULL,
                                    name_uz CHARACTER VARYING(200) UNIQUE NOT NULL ,
                                    name_ru CHARACTER VARYING(200) UNIQUE NOT NULL ,
                                    name_en CHARACTER VARYING(200) UNIQUE NOT NULL ,
                                    description_uz TEXT,
                                    description_ru TEXT,
                                    description_en TEXT,
                                    is_deleted BOOLEAN DEFAULT FALSE,
                                    price INTEGER,
                                    photo TEXT,
                                    category_id INTEGER REFERENCES Categories(id) ON DELETE SET NULL
                                    
                                )""")

            self.cur.execute("""CREATE TABLE IF NOT EXISTS Orders(
                                    id SERIAL PRIMARY KEY NOT NULL,
                                    quantity INTEGER ,
                                    amount BIGINT,
                                    date_order TIMESTAMP WITHOUT TIME ZONE,
                                    product_id INTEGER REFERENCES Products(id) ON DELETE SET NULL,
                                    user_id INTEGER REFERENCES Users(id) ON DELETE SET NULL
                                    )""")
            self.conn.commit()

    def add_user(self, user_id, user_name, message_date):
        with self.conn:
            self.cur.execute(f"SELECT id FROM Users WHERE id_tg={user_id}")
            id_data = self.cur.fetchone()
            if id_data is None:
                date_login = datetime.fromtimestamp(message_date).strftime('%d-%m-%y %H:%M:%S')
                self.cur.execute("INSERT INTO Users(id_tg, username, date_reg) VALUES(%s,%s,%s);",
                                 (user_id, user_name, date_login))
                self.cur.execute("INSERT INTO users_information(user_id) VALUES "
                                 "((SELECT id FROM users WHERE id_tg = %s))", (user_id, ))
                self.conn.commit()
            else:
                return
            return id_data

    def del_user(self, user_id):
        with self.conn:
            self.cur.execute("DELETE FROM Users WHERE id_tg = %s;", (user_id,))
            self.conn.commit()

    def add_user_contact(self, user_id, user_phone):
        with self.conn:
            self.cur.execute("UPDATE Users SET phone_numb = %s WHERE id_tg =%s;", (user_phone, user_id,))
            self.conn.commit()

    def get_user_temp(self, user_id):
        with self.conn:
            self.cur.execute("SELECT temp FROM users_information WHERE user_id = "
                             "(SELECT id FROM users WHERE id_tg = %s)", (user_id, ))
            return self.cur.fetchone()[0]

    def set_user_temp(self, user_id, temp):
        with self.conn:
            self.cur.execute("UPDATE users_information SET temp = %s WHERE user_id = "
                             "(SELECT id FROM users WHERE id_tg = %s)", (temp, user_id,))
            self.conn.commit()

    def get_user_lang(self, user_id):
        with self.conn:
            self.cur.execute("SELECT lang FROM users_information WHERE user_id = "
                             "(SELECT id FROM users WHERE id_tg = %s)", (user_id,))
            return self.cur.fetchone()[0]

    def set_user_lang(self, user_id, lang):
        with self.conn:
            self.cur.execute("UPDATE users_information SET lang = %s WHERE user_id = "
                             "(SELECT id FROM users WHERE id_tg = %s)", (lang, user_id,))
            self.conn.commit()

    def create_order(self, date_order, user_id):
        with self.conn:
            self.cur.execute("INSERT INTO orders(quantity, amount, date_order, product_id ,user_id)  "
                             "VALUES((SELECT last_chosen_quantity FROM users_information WHERE user_id = (SELECT id FROM users WHERE id_tg = %s)), "
                             "(SELECT last_chosen_quantity FROM users_information WHERE user_id = (SELECT id FROM users WHERE id_tg = %s)) * (SELECT price FROM products WHERE id = (SELECT last_chosen_product_id FROM users_information WHERE user_id = (SELECT id FROM users WHERE id_tg = %s)) ),"
                             "%s, "
                             "(SELECT last_chosen_product_id FROM users_information WHERE user_id = "
                             "(SELECT id FROM users WHERE id_tg = %s)), (SELECT id FROM users WHERE id_tg = %s))",
                             (user_id, user_id, user_id, date_order, user_id, user_id))
            self.conn.commit()

    def set_location(self, latitude, longitude, user_id):
        with self.conn:
            self.cur.execute("UPDATE users_information SET latitude = %s, longitude = %s  WHERE user_id = "
                             "(SELECT id FROM users WHERE id_tg = %s)", (latitude, longitude, user_id))
            self.conn.commit()

    def set_name_n_surname(self, name, surname, user_id):
        with self.conn:
            self.cur.execute("UPDATE Users SET name = %s, surname = %s  WHERE id_tg = %s",
                             (name, surname, user_id))
            self.conn.commit()

    def get_name_n_surname(self, user_id):
        with self.conn:
            self.cur.execute("SELECT name, surname FROM users WHERE id_tg = %s", (user_id, ))
            return self.cur.fetchone()

    def get_order_for_sending_to_channel(self, user_id):
        with self.conn:
            self.cur.execute("SELECT id, amount, quantity, date_order, "
                             "(SELECT name FROM users WHERE id_tg = %s), (SELECT surname FROM users WHERE id_tg = %s),"
                             "(SELECT phone_numb FROM users WHERE id_tg = %s), "
                             "(SELECT latitude FROM users_information WHERE user_id = "
                             "(SELECT id FROM users WHERE id_tg = %s)), "
                             "(SELECT longitude FROM users_information WHERE user_id = "
                             "(SELECT id FROM users WHERE id_tg = %s)),"
                             "(SELECT name_ru FROM products WHERE id = orders.product_id)"
                             "FROM orders WHERE id = (SELECT MAX(id) FROM orders WHERE user_id = "
                             "(SELECT id FROM users WHERE id_tg = %s)) ",
                             (user_id, user_id, user_id, user_id, user_id, user_id))
            return self.cur.fetchone()

    def cancel_order(self, user_id):
        with self.conn:
            self.cur.execute("DELETE FROM orders WHERE id = (SELECT MAX(id) WHERE user_id = "
                             "(SELECT id FROM users WHERE id_tg = %s))", (user_id, ))
            self.conn.commit()

    def get_all_categories(self, lang):
        with self.conn:
            if lang == 'uz':
                self.cur.execute(f"SELECT name_uz FROM categories WHERE is_deleted = False")
            elif lang == 'ru':
                self.cur.execute(f"SELECT name_ru FROM categories WHERE is_deleted = False")
            else:
                self.cur.execute(f"SELECT name_en FROM categories WHERE is_deleted = False")
            return [categ[0] for categ in self.cur.fetchall()]

    def get_products_name_by_category(self, user_id, lang):
        with self.conn:
            if lang == 'uz':
                self.cur.execute(f"SELECT name_uz FROM products WHERE is_deleted = False "
                                 f"AND category_id = (SELECT id FROM categories WHERE id = "
                                 f"(SELECT last_chosen_category_id FROM users_information WHERE user_id = "
                                 f"(SELECT id FROM users WHERE id_tg = %s)))", (user_id, ))
            elif lang == 'ru':
                self.cur.execute(f"SELECT name_ru FROM products WHERE is_deleted = False "
                                 f"AND category_id = (SELECT id FROM categories WHERE id = "
                                 f"(SELECT last_chosen_category_id FROM users_information WHERE user_id = "
                                 f"(SELECT id FROM users WHERE id_tg = %s)))", (user_id,))
            else:
                self.cur.execute(f"SELECT name_en FROM products WHERE is_deleted = False "
                                 f"AND category_id = (SELECT id FROM categories WHERE id = "
                                 f"(SELECT last_chosen_category_id FROM users_information WHERE user_id = "
                                 f"(SELECT id FROM users WHERE id_tg = %s)))", (user_id,))
            return [el[0] for el in self.cur.fetchall()]

    def set_last_product(self, user_id, product_name):
        with self.conn:
            self.cur.execute(f"UPDATE users_information SET last_chosen_product_id = "
                             f"(SELECT id FROM products WHERE name_uz = %s OR name_ru = %s) WHERE user_id = "
                             f"(SELECT id FROM users WHERE id_tg = %s)", (product_name, product_name, user_id))
            self.conn.commit()

    def set_last_category(self, user_id, product_name):
        with self.conn:
            self.cur.execute(f"UPDATE users_information SET last_chosen_category_id = "
                             f"(SELECT id FROM categories WHERE name_uz = %s OR name_ru = %s) WHERE user_id = "
                             f"(SELECT id FROM users WHERE id_tg = %s)", (product_name, product_name, user_id))
            self.conn.commit()

    def set_last_quantity(self, user_id, quantity):
        with self.conn:
            self.cur.execute(f"UPDATE users_information SET last_chosen_quantity = %s WHERE user_id = "
                             f"(SELECT id FROM users WHERE id_tg = %s)", (quantity, user_id))
            self.conn.commit()

    def get_product_info(self, user_id, lang):
        with self.conn:
            if lang == 'uz':
                self.cur.execute(f"SELECT name_uz, description_uz, price, photo FROM products WHERE is_deleted = False "
                                 f"AND id = (SELECT last_chosen_product_id FROM users_information WHERE user_id = "
                                 f"(SELECT id FROM users WHERE id_tg = %s))", (user_id,))
            elif lang == 'ru':
                self.cur.execute(f"SELECT name_ru, description_ru, price, photo FROM products WHERE is_deleted = False "
                                 f"AND id = (SELECT last_chosen_product_id FROM users_information WHERE user_id = "
                                 f"(SELECT id FROM users WHERE id_tg = %s))", (user_id,))
            else:
                self.cur.execute(f"SELECT name_en, description_en, price, photo FROM products WHERE is_deleted = False "
                                 f"AND id = (SELECT last_chosen_product_id FROM users_information WHERE user_id = "
                                 f"(SELECT id FROM users WHERE id_tg = %s))", (user_id,))
            return self.cur.fetchone()

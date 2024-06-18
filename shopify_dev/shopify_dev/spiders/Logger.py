import psycopg2

class Logger():
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"Не удалось подключиться к Базе данных: {e}")

        devs = self.get_developers()
        apps = self.get_apps()
        categories = self.get_categories()
    
    def insert_app(self, dev_info, name, rating, reviews, tag, launched) -> None:

        dev_id = self.insert_new_dev(dev_info)
        print(dev_id)

        try:
            values = (name, dev_id, rating, reviews, tag, launched)
            self.cur.execute("""INSERT INTO apps(name, dev_id, rating, reviews, tag, launched)
                                VALUES (%s, %s, %s, %s, %s, %s)""", values)
            self.conn.commit()
            return True, f"Apps inserted successfully"
        except Exception as error:
            print(f"Error while inserting Developer: {error}")
            return False, f"Error while inserting Apps: {error}"

    def insert_new_dev(self, dev_info) -> str:
        name = dev_info[0]
        apps = dev_info[1]
        rating = dev_info[2]
        years = dev_info[3]
        country = dev_info[4]
        email = dev_info[5]

        if check_developer_in_devs():
            return check_developer_in_devs

        try:
            values = (name, apps, rating, years, country, email)
            self.cur.execute("""INSERT INTO developers(name, apps, rating, years, country, email)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                RETURNING dev_id""", values)
            self.conn.commit()
            dev_id = self.cur.fetchone()[0]
            return dev_id
        except Exception as error:
            print(f"Error while inserting Developer: {error}")
            return False

    def insert_new_category(self, category, url) -> None:
        try:
            values = (category, url)
            self.cur.execute("""INSERT INTO categories(name, url)
                                VALUES (%s, %s)""", values)
            self.conn.commit()
            return True, f"Category inserted successfully"
        except Exception as error:
            print(f"Error while inserting category: {error}")
            return False, f"Error while inserting category: {error}"

    def check_developers_exist(self, name) -> str:
        pass

    def get_categories(self):
        pass
    
    def get_developers(self) -> list:
        apps = self.cur.execute("""SELECT name FROM developers""")
        return list

    def get_apps(self):
        pass

db = Logger(dbname="EpsiFund", user="postgres", password="1234", host="localhost", port="5432")

db.insert_app(("name", 15, 4.3, 10, "US", "email"), "Prisync", 4.5, 300, True, 8)
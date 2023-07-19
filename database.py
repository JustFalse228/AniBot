import sqlite3 as sq
import os


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS "users" (
	"id" INTEGER UNIQUE,
    "reg_date" TEXT,
    "viewed_titles" INTEGER DEFAULT 0,
    "current_view_titles" INTEGER DEFAULT 0,
    "titles" TEXT DEFAULT NULL,
    "cur_view" TEXT DEFAULT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
"""


class Database:
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(path, "database.db")):
            self.conn = sq.connect(os.path.join(path, "database.db"))
            cur = self.conn.cursor()
            cur.executescript(CREATE_SQL)
            cur.close()
            self.conn.commit()
        else:
            self.conn = sq.connect(os.path.join(path, "database.db"))

    def check_user_db(self, user_id):
        cur = self.conn.cursor()
        check = cur.execute("SELECT reg_date FROM users WHERE id = ?", (user_id,))
        user = check.fetchone()
        cur.close()
        return bool(user)

    def check_user(self, user_id):
        cur = self.conn.cursor()
        result = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_info = result.fetchall()
        for user in user_info:
            id = user[0]
            reg_date = user[1]
            viewed_titles = user[2]
            current_view = user[3]
        cur.close()
        return id, reg_date, viewed_titles, current_view

    def add_user(self, user_id, time):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO users(id, reg_date) VALUES (?,?);", (user_id, time))
        cur.close()
        self.conn.commit()

    def add_to_viewed(self, title_name, ids):
        cur = self.conn.cursor()
        cur.execute("SELECT titles FROM users WHERE id = ?", (ids,))
        row = cur.fetchone()

        if row[0] != "" and row[0] != " " and row[0] != None:
            existing_text = row[0]
            update_title = str(existing_text) + ";" + title_name
            cur.execute("UPDATE users SET titles = ? WHERE id = ?", (update_title, ids))
            self.conn.commit()
            cur.close()
        else:
            cur.execute("UPDATE users SET titles = ? WHERE id = ?", (title_name, ids))
            self.conn.commit()
            cur.close()

    def get_titles(self, id):
        cur = self.conn.cursor()
        cur.execute("SELECT titles FROM users WHERE id = ?", (id,))
        return cur.fetchone()[0]
    
    def remove_title(self, id, titles):
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET titles = ? WHERE id = ?", (titles, id))
        self.conn.commit()
        cur.close()
    
    def remove_cur_title(self, id, titles):
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET cur_view = ? WHERE id = ?", (titles, id))
        self.conn.commit()
        cur.close()

    def add_view_title(self, id):
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET viewed_titles = viewed_titles + ? WHERE id = ?", (1, id,))
        self.conn.commit()
        cur.close()

    def add_cur_view(self, title_name, ids):
        cur = self.conn.cursor()
        cur.execute("SELECT cur_view FROM users WHERE id = ?", (ids,))
        row = cur.fetchone()

        if row[0] != "" and row[0] != " " and row[0] != None:
            existing_text = row[0]
            update_title = str(existing_text) + ";" + title_name
            cur.execute("UPDATE users SET cur_view = ? WHERE id = ?", (update_title, ids))
            self.conn.commit()
            cur.close()
        else:
            cur.execute("UPDATE users SET cur_view = ? WHERE id = ?", (title_name, ids))
            self.conn.commit()
            cur.close()
    
    def get_cur_view(self, id):
        cur = self.conn.cursor()
        cur.execute("SELECT cur_view FROM users WHERE id = ?", (id,))
        return cur.fetchone()[0]

    def add_current_profile(self, id):
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET current_view_titles = current_view_titles + ? WHERE id = ?", (1, id,))
        self.conn.commit()
        cur.close()

    def minus_viewed_titles(self, id):
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET viewed_titles = viewed_titles - ? WHERE id = ?", (1, id,))
        self.conn.commit()
        cur.close()

    def minus_cur_view(self, id):
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET current_view_titles = current_view_titles - ? WHERE id = ?", (1, id,))
        self.conn.commit()
        cur.close()
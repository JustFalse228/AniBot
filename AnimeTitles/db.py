import psycopg2


def make_connect():
    connection = psycopg2.connect(
        database="postgres",
        user="postgres",
        host="127.0.0.1",
        password="qwerty",
    )
    connection.autocommit = True
    return connection


def create_titles():
    c = make_connect()
    cursor = c.cursor()
    cursor.execute("CREATE TABLE titles(id serial PRIMARY KEY, name TEXT UNIQUE, view int default 0, viewed int default 0, request TEXT);")
    cursor.close()


def add_title(name, request):
    cursor = make_connect().cursor()
    cursor.execute("INSERT INTO titles(name, request) VALUES (%s, %s)",(name, request,))
    cursor.close()


def get_title_id(name):
    cursor = make_connect().cursor()
    cursor.execute("SELECT id FROM titles WHERE name = %s", (name,))
    result = cursor.fetchone()[0]
    return result


def get_titles_views(name):
    cursor = make_connect().cursor()
    cursor.execute("SELECT view, viewed FROM titles WHERE name = %s", (name,))

    return cursor.fetchone()


def get_title_for_id(id):
    cursor = make_connect().cursor()
    cursor.execute("SELECT name FROM titles WHERE id = %s", (id,))
    result = cursor.fetchone()[0]
    return result


def get_url(id):
    cursor = make_connect().cursor()
    cursor.execute("SELECT request FROM titles WHERE id = %s", (id,))
    result = cursor.fetchone()[0]
    return result

def add_viewed(id):
    cursor = make_connect().cursor()
    cursor.execute("UPDATE titles SET viewed = viewed + %s WHERE id = %s", (1, id))
    cursor.close()

def add_view(id):
    cursor = make_connect().cursor()
    cursor.execute("UPDATE titles SET view = view + %s WHERE id = %s", (1, id))
    cursor.close()
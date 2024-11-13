import sqlite3

DATABASE = 'users.db'


# Initialize the database and create the users table
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def get_all_usr():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


# Filter by name and age range
def get_users_by_name_and_age(name_query, min_age, max_age):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE name LIKE ?"
    params = ['%' + name_query + '%']

    if min_age:
        query += " AND age >= ?"
        params.append(min_age)

    if max_age:
        query += " AND age <= ?"
        params.append(max_age)

    cursor.execute(query, tuple(params))
    users = cursor.fetchall()
    conn.close()
    return users


def add_usr(name, age):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

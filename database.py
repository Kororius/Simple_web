import sqlite3

DATABASE = 'users.db'


# Initialize the database and create the users, departments, and employees tables
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints

    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    # Create departments table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create employees table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
    ''')

    conn.commit()
    conn.close()


def add_department(name):
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO departments (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def add_employee(name, age, department_id):
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")  # Ensure foreign keys are enabled
    cursor = conn.cursor()
    try:
        # Attempt to insert employee record
        cursor.execute("INSERT INTO employees (name, age, department_id) VALUES (?, ?, ?)", (name, age, department_id))
        conn.commit()
        print(f"Added employee: Name={name}, Age={age}, Department ID={department_id}")
    except sqlite3.IntegrityError as e:
        # Print error if foreign key constraint or other database issue arises
        print(f"Error adding employee: {e}")
    finally:
        conn.close()


def get_all_departments():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()
    conn.close()
    return departments


def get_employees_by_department(department_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE department_id = ?", (department_id,))
    employees = cursor.fetchall()
    conn.close()
    return employees


# Existing user functions
def get_all_usr():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


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
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()
def get_all_employees():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return employees

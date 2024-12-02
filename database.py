"""
This module provides functions to manage the database,
including initializing tables and performing CRUD operations for users,
departments, and employees.
"""

import sqlite3

DATABASE = 'users.db'


def init_db():
    """
    Initialize the database and create the users, departments, and employees tables.
    Ensures foreign key constraints are enabled.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
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
    """
    Add a new department to the database.

    Args:
        name (str): The name of the department.
    """
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO departments (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def add_employee(name, age, department_id):
    """
    Add a new employee to a specific department in the database.

    Args:
        name (str): Employee's name.
        age (int): Employee's age.
        department_id (int): ID of the department the employee belongs to.
    """
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO employees (name, age, department_id)
            VALUES (?, ?, ?)
            """,
            (name, age, department_id)
        )
        conn.commit()
        print(f"Added employee: Name={name}, Age={age}, Department ID={department_id}")
    except sqlite3.IntegrityError as e:
        print(f"Error adding employee: {e}")
    finally:
        conn.close()


def get_all_departments():
    """
    Retrieve all departments from the database.

    Returns:
        list: A list of tuples containing department data.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()
    conn.close()
    return departments


def get_employees_by_department(department_id):
    """
    Retrieve all employees belonging to a specific department.

    Args:
        department_id (int): The ID of the department.

    Returns:
        list: A list of tuples containing employee data.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE department_id = ?", (department_id,))
    employees = cursor.fetchall()
    conn.close()
    return employees


def get_all_usr():
    """
    Retrieve all users from the database.

    Returns:
        list: A list of tuples containing user data.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def get_users_by_name_and_age(name_query, min_age, max_age):
    """
    Retrieve users based on name and age range.

    Args:
        name_query (str): A substring to search in user names.
        min_age (int): The minimum age for filtering users.
        max_age (int): The maximum age for filtering users.

    Returns:
        list: A list of tuples containing filtered user data.
    """
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
    """
    Retrieve all employees from the database.

    Returns:
        list: A list of tuples containing employee data.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return employees

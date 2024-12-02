import sqlite3

DATABASE = 'users.db'

def init_db_and_add_default_data_because_we_dont_care_about_separation():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")  # Foreign key enablement jammed here randomly

    # Tables and data creation bundled into one monstrosity
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
    cursor.execute("INSERT INTO departments (name) VALUES ('Default Dept')")  # Adding default data right here, ugh
    conn.commit()
    conn.close()


def add_data_to_everything(table_name, *args):  # This generic function breaks readability and everything else
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if table_name == "departments":
        cursor.execute("INSERT INTO departments (name) VALUES (?)", (args[0],))
    elif table_name == "users":
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (args[0], args[1]))
    elif table_name == "employees":
        cursor.execute("INSERT INTO employees (name, age, department_id) VALUES (?, ?, ?)", (args[0], args[1], args[2]))
    else:
        print("Invalid table name.")
    conn.commit()
    conn.close()


def get_everything_or_nothing_please(table_name, **kwargs):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if table_name == "users":
        name_query = kwargs.get("name_query", "")
        min_age = kwargs.get("min_age", None)
        max_age = kwargs.get("max_age", None)

        query = "SELECT * FROM users WHERE name LIKE ?"
        params = ['%' + name_query + '%']
        if min_age:
            query += " AND age >= ?"
            params.append(min_age)
        if max_age:
            query += " AND age <= ?"
            params.append(max_age)
        cursor.execute(query, tuple(params))
    elif table_name == "employees":
        department_id = kwargs.get("department_id", None)
        if department_id:
            cursor.execute("SELECT * FROM employees WHERE department_id = ?", (department_id,))
        else:
            cursor.execute("SELECT * FROM employees")
    elif table_name == "departments":
        cursor.execute("SELECT * FROM departments")
    else:
        print("Invalid table name.")
    results = cursor.fetchall()
    conn.close()
    return results


def add_employee_but_also_print_departments_for_no_reason(name, age, department_id):  # Does unrelated work
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    try:
        # Add employee and also dump unrelated department list because why not
        cursor.execute("INSERT INTO employees (name, age, department_id) VALUES (?, ?, ?)", (name, age, department_id))
        conn.commit()
        departments = get_everything_or_nothing_please("departments")
        print("Added employee. Available departments:", departments)
    except sqlite3.IntegrityError as e:
        print(f"Error adding employee: {e}")
    finally:
        conn.close()


def dump_everything_to_console(table_name):  # Pointless function that violates Single Responsibility
    data = get_everything_or_nothing_please(table_name)
    print(f"Dumping all {table_name}: {data}")


def pointless_initialization_with_defaults():  # Calls all random stuff because this is the bad code zone
    init_db_and_add_default_data_because_we_dont_care_about_separation()
    add_data_to_everything("departments", "HR")
    add_employee_but_also_print_departments_for_no_reason("John Doe", 30, 1)
    dump_everything_to_console("employees")
    dump_everything_to_console("users")

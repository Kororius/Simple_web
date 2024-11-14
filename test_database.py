import unittest
import sqlite3
from database import *

class TestDatabaseOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the database for tests, called once before any tests run."""
        # Initialize the database and create the tables
        init_db()

    @classmethod
    def tearDownClass(cls):
        """Clean up the database after all tests run."""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        # Drop all tables to ensure clean state for subsequent tests
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS departments")
        cursor.execute("DROP TABLE IF EXISTS employees")
        conn.commit()
        conn.close()

    def setUp(self):
        """Reset the database before each test."""
        # Clear out the data from the tables to ensure each test is isolated
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM departments")
        cursor.execute("DELETE FROM employees")
        conn.commit()
        conn.close()

    def test_add_user(self):
        """Test adding a user."""
        add_usr("John Doe", 30)
        users = get_all_usr()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][1], "John Doe")
        self.assertEqual(users[0][2], 30)

    def test_add_department(self):
        """Test adding a department."""
        add_department("HR")
        departments = get_all_departments()
        self.assertEqual(len(departments), 1)
        self.assertEqual(departments[0][1], "HR")

    def test_add_employee(self):
        """Test adding an employee to a department."""
        # First, add a department
        add_department("Engineering")
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM departments WHERE name = 'Engineering'")
        department_id = cursor.fetchone()[0]
        conn.close()

        # Add an employee to that department
        add_employee("Alice Smith", 25, department_id)
        employees = get_employees_by_department(department_id)
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0][1], "Alice Smith")
        self.assertEqual(employees[0][2], 25)
        self.assertEqual(employees[0][3], department_id)

    def test_get_users_by_name_and_age(self):
        """Test retrieving users by name and age range."""
        add_usr("John Doe", 30)
        add_usr("Jane Doe", 25)
        add_usr("Jake Smith", 40)

        users = get_users_by_name_and_age("Doe", 20, 35)
        self.assertEqual(len(users), 2)
        self.assertIn("John Doe", [user[1] for user in users])
        self.assertIn("Jane Doe", [user[1] for user in users])

    def test_get_employees_by_department(self):
        """Test retrieving employees by department."""
        # Add a department
        add_department("Marketing")
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM departments WHERE name = 'Marketing'")
        department_id = cursor.fetchone()[0]
        conn.close()

        # Add employees to the department
        add_employee("Jack Johnson", 35, department_id)
        add_employee("Jill Jackson", 28, department_id)

        employees = get_employees_by_department(department_id)
        self.assertEqual(len(employees), 2)
        self.assertEqual(employees[0][1], "Jack Johnson")
        self.assertEqual(employees[1][1], "Jill Jackson")

if __name__ == '__main__':
    unittest.main()

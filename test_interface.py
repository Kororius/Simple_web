import unittest
from flask import Flask

from database import *
from interface import app
from flask_testing import TestCase

class TestFlaskRoutes(TestCase):

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
        """Reset the database before each test, including auto-increment counters."""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM departments")
        cursor.execute("DELETE FROM employees")
        # Reset auto-increment for each table
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='departments'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='employees'")
        conn.commit()
        conn.close()

    def create_app(self):
        # Set up the Flask app for testing
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_users.db'  # Ensure Flask uses the test DB
        return app

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Simple Web App", response.data)

    def test_add_user_page(self):
        response = self.client.get('/add_user')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add User", response.data)

    def test_add_user_post(self):
        response = self.client.post('/add_user', data={'name': 'John', 'age': '30'})
        self.assertEqual(response.status_code, 302)

    def test_add_department_page(self):
        response = self.client.get('/add_department')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add Department", response.data)

    def test_add_employee_page(self):
        # Test that departments are available on the add_employee page
        response = self.client.get('/add_employee')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add Employee", response.data)

    def test_add_employee_post(self):
        # Add department and employee
        self.client.post('/add_department', data={'name': 'HR'})
        response = self.client.post('/add_employee', data={'name': 'Alice', 'age': '25', 'department_id': '1'})
        self.assertEqual(response.status_code, 302)

    def test_list_employees(self):
        # Test employees listing with GET
        self.client.post('/add_department', data={'name': 'HR'})
        self.client.post('/add_employee', data={'name': 'Alice', 'age': '25', 'department_id': '1'})
        response = self.client.get('/employees?department_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"HR", response.data)
        self.assertIn(b"Alice", response.data)

if __name__ == '__main__':
    unittest.main()

"""
This module defines the Flask application for managing users, departments, and employees.
It includes routes for adding and retrieving data from the database.
"""
import sqlite3

from flask import Flask, request, render_template, redirect, url_for
from database import init_db, add_usr, get_users_by_name_and_age, add_department, add_employee, get_all_departments, \
    get_employees_by_department, get_all_employees

app = Flask(__name__)
init_db()

@app.route('/')
def home():
    """
    Render the home page of the application.

    Returns:
        str: The HTML content for the home page.
    """
    return render_template('home.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Add a new user to the database via a form submission.

    Returns:
        str: Redirects to the home page on successful form submission or renders the form.
    """
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        add_usr(name, age)
        return redirect(url_for('home'))
    return render_template('add_user.html')

@app.route('/get_users', methods=['GET'])
def get_users():
    """
    Retrieve and display users filtered by search query and age range.

    Returns:
        str: The HTML content displaying the filtered user list.
    """
    search_query = request.args.get('search', '')
    min_age = request.args.get('min_age', '')
    max_age = request.args.get('max_age', '')
    users = get_users_by_name_and_age(search_query, min_age, max_age)
    return render_template('users_list.html', users=users)

@app.route('/add_department', methods=['GET', 'POST'])
def add_department_route():
    """
    Add a new department to the database via a form submission.

    Returns:
        str: Redirects to the home page on successful form submission or renders the form.
    """
    if request.method == 'POST':
        name = request.form['name']
        add_department(name)
        return redirect(url_for('home'))
    return render_template('add_department.html')

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee_route():
    """
    Add a new employee to the database via a form submission.
    Associates the employee with a department.

    Returns:
        str: Redirects to the employee list page or renders the form.
    """
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        department_id = request.form['department_id']
        add_employee(name, age, department_id)
        return redirect(url_for('list_employees', department_id=department_id))

    departments = get_all_departments()
    return render_template('add_employee.html', departments=departments)

@app.route('/employees', methods=['GET'])
def list_employees():
    """
    Display a list of employees filtered by department.

    Returns:
        str: The HTML content displaying the employee list and departments.
    """
    department_id = request.args.get('department_id')
    if department_id:
        employees = get_employees_by_department(department_id)
    else:
        # If no department_id is provided, fetch all employees
        employees = get_all_employees()  # You should implement this method to fetch all employees

    departments = get_all_departments()
    return render_template('employees_list.html', employees=employees, departments=departments)

if __name__ == '__main__':
    app.run(debug=True)

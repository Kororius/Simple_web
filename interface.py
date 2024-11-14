from flask import Flask, request, render_template, redirect, url_for
from database import init_db, add_usr, get_users_by_name_and_age, add_department, add_employee, get_all_departments, \
    get_employees_by_department, get_all_employees

app = Flask(__name__)
init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        add_usr(name, age)
        return redirect(url_for('home'))
    return render_template('add_user.html')

@app.route('/get_users', methods=['GET'])
def get_users():
    search_query = request.args.get('search', '')
    min_age = request.args.get('min_age', '')
    max_age = request.args.get('max_age', '')
    users = get_users_by_name_and_age(search_query, min_age, max_age)
    return render_template('users_list.html', users=users)

@app.route('/add_department', methods=['GET', 'POST'])
def add_department_route():
    if request.method == 'POST':
        name = request.form['name']
        add_department(name)
        return redirect(url_for('home'))
    return render_template('add_department.html')

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee_route():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        department_id = request.form['department_id']
        add_employee(name, age, department_id)
        # After adding the employee, redirect to the list of employees
        return redirect(url_for('list_employees', department_id=department_id))

    departments = get_all_departments()
    return render_template('add_employee.html', departments=departments)


@app.route('/employees', methods=['GET'])
@app.route('/employees', methods=['GET'])
def list_employees():
    department_id = request.args.get('department_id')

    # If no department is selected, show all employees
    if department_id:
        employees = get_employees_by_department(department_id)
    else:
        # If no department_id is provided, fetch all employees
        employees = get_all_employees()  # You should implement this method to fetch all employees

    departments = get_all_departments()
    return render_template('employees_list.html', employees=employees, departments=departments)

if __name__ == '__main__':
    app.run(debug=True)

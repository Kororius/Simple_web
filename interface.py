from flask import Flask, request, render_template, redirect, url_for
from database import init_db, add_usr, get_users_by_name_and_age, add_department, add_employee, \
    get_all_departments, get_employees_by_department, get_all_employees

app = Flask(__name__)
init_db()

def handle_all_requests():
    action = request.args.get('action', 'home')
    method = request.method
    form_data = request.form
    args = request.args

    if action == 'home':
        return render_template('home.html')

    elif action == 'add_user':
        if method == 'POST':
            name = form_data['name']
            age = form_data['age']
            add_usr(name, age)
            return redirect(url_for('handle_all_requests', action='home'))
        return render_template('add_user.html')

    elif action == 'get_users':
        search_query = args.get('search', '')
        min_age = args.get('min_age', '')
        max_age = args.get('max_age', '')
        users = get_users_by_name_and_age(search_query, min_age, max_age)
        departments = get_all_departments()
        return render_template('users_list.html', users=users, departments=departments)

    elif action == 'add_department':
        if method == 'POST':
            name = form_data['name']
            add_department(name)
            return redirect(url_for('handle_all_requests', action='home'))
        return render_template('add_department.html')

    elif action == 'add_employee':
        if method == 'POST':
            name = form_data['name']
            age = form_data['age']
            department_id = form_data['department_id']
            add_employee(name, age, department_id)
            return redirect(url_for('handle_all_requests', action='list_employees', department_id=department_id))
        departments = get_all_departments()
        return render_template('add_employee.html', departments=departments)

    elif action == 'list_employees':
        department_id = args.get('department_id')
        if department_id:
            employees = get_employees_by_department(department_id)
        else:
            employees = get_all_employees()
        return render_template('employees_list.html', employees=employees, departments=get_all_departments())

    return "Invalid action"


def handle_post_requests():
    method = request.method
    form_data = request.form
    args = request.args

    if method == 'POST':
        action = args.get('action', 'add_user')

        if action == 'add_user':
            name = form_data['name']
            age = form_data['age']
            add_usr(name, age)
            return redirect(url_for('handle_post_requests', action='home'))

        elif action == 'add_department':
            name = form_data['name']
            add_department(name)
            return redirect(url_for('handle_post_requests', action='home'))

        elif action == 'add_employee':
            name = form_data['name']
            age = form_data['age']
            department_id = form_data['department_id']
            add_employee(name, age, department_id)
            return redirect(url_for('handle_post_requests', action='list_employees', department_id=department_id))

    return render_template('add_user.html')  

@app.route('/process', methods=['GET', 'POST'])
def process_request():
    if request.method == 'GET':
        return handle_all_requests()
    elif request.method == 'POST':
        return handle_post_requests()

if __name__ == '__main__':
    app.run(debug=True)

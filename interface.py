from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from database import init_db, add_usr, get_users_by_name_and_age, DATABASE  # Ensure all necessary functions are imported

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
        # Removed the city field
        add_usr(name, age)  # Now only passing name and age to the add_usr function
        return redirect(url_for('home'))  # Redirect to the home page after form submission
    return render_template('add_user.html')

@app.route('/get_users', methods=['GET'])
def get_users():
    search_query = request.args.get('search', '')  # Get the search query
    min_age = request.args.get('min_age', '')  # Get the minimum age filter
    max_age = request.args.get('max_age', '')  # Get the maximum age filter

    # Call the function that applies the filters
    users = get_users_by_name_and_age(search_query, min_age, max_age)

    return render_template('users_list.html', users=users)

def get_users_by_name_and_age(name_query, min_age, max_age):
    # Use an empty string if name_query is None
    if name_query is None:
        name_query = ''

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Build the query dynamically based on provided filters
    query = "SELECT * FROM users WHERE name LIKE ?"
    params = ['%' + name_query + '%']  # Safe concatenation since name_query is never None

    if min_age:
        query += " AND age >= ?"
        params.append(int(min_age))  # Ensure min_age is cast to int

    if max_age:
        query += " AND age <= ?"
        params.append(int(max_age))  # Ensure max_age is cast to int

    cursor.execute(query, tuple(params))
    users = cursor.fetchall()
    conn.close()
    return users

# The add_usr function now only takes name and age as parameters
def add_usr(name, age):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)

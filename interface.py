from flask import Flask, request, render_template, redirect, url_for
from database import init_db, add_usr, get_all_usr, get_users_by_name_and_age
from models import Persn

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


if __name__ == '__main__':
    app.run(debug=True)

import sqlite3
from flask import Flask, render_template, Response, request, jsonify
import os

app = Flask(__name__, template_folder='./templates1')
currentdir = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def main_page():
    return render_template('register.html')


# @app.route('/', methods=['POST', 'GET'])
# def data_entry():
#     # if request.method == 'POST':

#     # return render_template('register.html')


@ app.route('/thankyou.html', methods=['POST'])
def ty():
    # id = request.form['id']
    i = request.form.get("id", False)
    # id = 123
    n = request.form.get("name", False)
    activity = request.form.get("activity_name", False)
    fname = request.form.get("filename", False)

    print(f"{i}, {n}, {activity}, {fname}")
    print(f"{type(i)}, {type(n)}, {type(activity)}, {type(fname)}")

    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    query = 'INSERT INTO test  VALUES (?, ?, ?, ?)'
    params = (i, n, activity, fname)
    # conn.execute(
    #     f"INSERT INTO test  VALUES ({i}, {n}, {activity}, {fname})")

    conn.execute(query, params)

    # conn.execute(
    #     f"INSERT INTO test (id,name,activity_name,filename) VALUES (123,'abc','pqr','xyz')")

    conn.commit()
    print("Records created successfully")
    conn.close()
    return render_template('thankyou.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector


app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)


# instagram link
@app.route('/insta')
def insta():
    return redirect("https://www.instagram.com/bengurionuniversity/?hl=en")


# facebook link
@app.route('/facebook')
def facebook():
    return redirect("https://www.facebook.com/BenGurionUniversity/")


###### PAGES
##HomePage
from assignment_4.HomePage.HomePage import HomePage

app.register_blueprint(HomePage)

##connect
from assignment_4.connect.connect import connect

app.register_blueprint(connect)

##assignment3_1
from assignment_4.assignment3_1.assignment3_1 import assignment3_1

app.register_blueprint(assignment3_1)

##assignment3_2
from assignment_4.assignment3_2.assignment3_2 import assignment3_2

app.register_blueprint(assignment3_2)

##assignment_4
from assignment_4.assignment_4.assignment4 import assignment_4

app.register_blueprint(assignment_4)


# ------------------------------------------------- #
# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #
def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='myflaskappdb')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    #

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


# ------------------------------------------------- #
# ------------------- SELECT ---------------------- #
# ------------------------------------------------- #
@app.route('/users')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('users.html', users=users_list)


# ------------------------------------------------- #
# -------------------- DELETE --------------------- #
# ------------------------------------------------- #
@app.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_id = request.form['user_id']
    query = "DELETE FROM users WHERE id='%s';" % user_id
    # print(query)
    interact_db(query, query_type='commit')
    return redirect('/users')


if __name__ == '__main__':
    app.run(debug=True)

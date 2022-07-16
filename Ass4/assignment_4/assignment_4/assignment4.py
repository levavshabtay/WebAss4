import random
from flask import Blueprint
from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify, json
import mysql.connector
import time
import requests

##########################################################################
##################################PART-A##################################
##########################################################################
assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='static',
                         static_url_path='/assignment4/outer_source',
                         template_folder='templates')


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
# -------------------- INSERT --------------------- #
# ------------------------------------------------- #
@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    session['Deletion'] = False
    session['Update'] = False
    session['Insertion'] = True
    name = request.form['name'].capitalize()
    nickname = request.form['nickname'].capitalize()
    email = request.form['email'].lower()
    id = request.form['id']
    check = "select * FROM users WHERE ID='%s';" % id
    users_list = interact_db(check, query_type='fetch')
    if len(users_list) > 0:
        session['insert_feedback'] = "sorry, this user is already in our DB "
    else:
        query = "INSERT INTO users(ID, email, name, nickName) VALUES ('%s','%s', '%s', '%s')" % (id, email, name, nickname)
        interact_db(query=query, query_type='commit')
        session['insert_feedback'] = "user inserted successfully :) "
    return redirect('/assignment4')


# ------------------------------------------------- #
# -------------------- DELETE --------------------- #
# ------------------------------------------------- #
@assignment_4.route('/delete_user', methods=['POST'])
def delete_user_func():
    session['Deletion'] = True
    session['Update'] = False
    session['Insertion'] = False
    id = request.form['id']
    check = 'select * from users'
    users_list_befor = interact_db(check, query_type='fetch')
    query = "DELETE FROM users WHERE ID='%s';" % id
    interact_db(query, query_type='commit')
    check = 'select * from users'
    users_list_after = interact_db(check, query_type='fetch')
    if len(users_list_befor) > len(users_list_after):
        session['delete_feedback'] = "user deleted successfully :) "
    else:
        session['delete_feedback'] = "sorry, there is no user with this ID in our DB"
    return redirect('/assignment4')


# ------------------------------------------------- #
# ------------------- UPDATE ---------------------- #
# ------------------------------------------------- #
@assignment_4.route('/update_user', methods=['POST'])
def update_user():
    session['Deletion'] = False
    session['Update'] = True
    session['Insertion'] = False
    id = request.form['id']
    email = request.form['email'].lower()
    name = request.form['name'].capitalize()
    nickname = request.form['nickname'].capitalize()
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='myflaskappdb')
    check = "select * FROM users WHERE ID='%s';" % id
    users_list = interact_db(check, query_type='fetch')
    if len(users_list) > 0:
        updateCursor = connection.cursor()
        updateCursor.execute('''
            UPDATE users
            SET name = %s, nickName = %s ,email = %s
            WHERE ID = %s
            ''', (name, nickname, email, id))
        connection.commit()
        session['update_feedback'] = "user info updated successfully :) "
    else:
        session['update_feedback'] = "sorry, we could not find user in our DB "
    return redirect('/assignment4')


# ------------------------------------------------- #
# ------------------- SELECT ---------------------- #
# ------------------------------------------------- #
@assignment_4.route('/assignment4')
def select_user():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users=users_list)


##########################################################################
##################################PART-B##################################
##########################################################################
@assignment_4.route('/assignment4/users')
def assignment4_users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    users_list_JSON = json.dumps(users_list)
    return render_template('users.html', users_json=users_list_JSON)


@assignment_4.route('/fetch_be')
def fetch_be_func():
    id = int(request.args['num_id'])
    session['num'] = id
    userByID = get_user_by_id(id)
    save_user_to_session(userByID)
    return redirect('/assignment4/outer_source')


@assignment_4.route('/assignment4/outer_source')
def fetch_fe_func():
    return render_template('outerSource.html')


def get_user_by_id(ID):
    userByID = []
    res = requests.get(f'https://reqres.in/api/users/{ID}')
    userByID.append(res.json())
    return userByID


def save_user_to_session(userByID):
    user_to_save = []
    for user in userByID:
        userByID = {'data': {'avatar': user['data']['avatar']},
                    'email': user['data']['email'],
                    'first_name': user['data']['first_name'], }
        user_to_save.append(userByID)
    session['userByID'] = user_to_save


##########################################################################
##################################PART-B##################################
##########################################################################
@assignment_4.route('/assignment4/restapi_users', defaults={'user_id': 318233210})
@assignment_4.route('/assignment4/restapi_users/<int:user_id>')
def assignment4_restapi_users(user_id):
    table = "select * FROM users WHERE ID='%s';" % user_id
    restapi_user_list = interact_db(table, query_type='fetch')
    if len(restapi_user_list) > 0:
        session['noID'] = False
        returnUser = json.dumps(restapi_user_list)
        return render_template('restapiUsers.html', user=returnUser)
    else:
        session['noID'] = True
        session['noID_message'] = json.dumps('no user with this id in our DB')
        return render_template('restapiUsers.html')

from flask import Blueprint, render_template
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request, session, jsonify

assignment3_2 = Blueprint('assignment3_2', __name__,
                          static_folder='static',
                          template_folder='templates')


# root of users - ass 3_2
@assignment3_2.route('/users', methods=['GET', 'POST'])
def users_page():
    # search form - get method
    if request.method == 'GET':
        if 'email' in request.args:
            email = request.args['email'].lower()
            if email in user_dict:
                return render_template('assignment3_2.html',
                                       name=user_dict[email][0],
                                       email=email,
                                       nickName=user_dict[email][1])
            if len(email) == 0:
                return render_template('assignment3_2.html',
                                       user_dict=user_dict)
            else:
                return render_template('assignment3_2.html', message1='sorry, User not exist ')

    # Post Case
    if request.method == 'POST':
        email = request.form['email'].lower()
        username = request.form['username']
        nickName = request.form['nickName']
        if email in user_dict:
            session['logedin'] = False
            return render_template('assignment3_2.html',
                                   message2='Hey there, you already registered!')
        else:
            session['username'] = username
            session['email'] = email
            session['nickName'] = nickName
            session['logedin'] = True
            user_dict[email] = (username, nickName)
            return render_template('assignment3_2.html')

    else:
        return render_template('assignment3_2.html')


@assignment3_2.route('/log_out')
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('users_page'))


@assignment3_2.route('/session')
def session_func():
    # print(session['CHECK'])
    return jsonify(dict(session))


user_dict = {
    'Levavs@gmail.com': ['Levav', 'levi'],
    'Benny@gmail.com': ['Benny', 'benjy'],
    'Tati@gmail.com': ['Tatiana', 'tati'],
    'Noam@gmail.com': ['Noam', 'nona'],
    'LinoyA@gmail.com': ['Linoy', 'lin']
}

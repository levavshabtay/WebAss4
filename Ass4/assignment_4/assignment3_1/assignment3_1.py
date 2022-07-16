from flask import Blueprint, render_template
from flask import session

assignment3_1 = Blueprint('assignment3_1', __name__,
                          static_folder='static',
                          template_folder='templates')


# root of about -- ass 3_1
@assignment3_1.route('/about')
def about_page():
    user_info = {'user_name': 'levav', 'second_name': 'shabtay', 'nick_name': 'lev',
                 'study': 'engineering'}
    hobbies = ('makeUp', 'dance', 'movies', 'TV', 'food making', 'sport')
    session['CHECK'] = 'about'
    return render_template('assignment3_1.html',
                           user_info=user_info,
                           hobbies=hobbies)

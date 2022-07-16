from flask import Blueprint, render_template

connect = Blueprint('connect', __name__,
                    static_folder='static',
                    template_folder='templates')


# root of contact us
@connect.route('/connect')
def connect_func():
    return render_template('connect.html')


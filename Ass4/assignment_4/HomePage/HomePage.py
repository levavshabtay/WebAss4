from flask import Blueprint, render_template

HomePage = Blueprint('HomePage', __name__,
                     static_folder='static',
                     static_url_path='/HomePage',
                     template_folder='templates')


# root of study buddy website
@HomePage.route('/')
def index_func():
    return render_template('homepage.html')

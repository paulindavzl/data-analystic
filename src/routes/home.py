from flask import Blueprint

home = Blueprint('home', __name__)


# página inicial do site
@home.route('/')
def homepage():
    return 'This is the home page for this website'
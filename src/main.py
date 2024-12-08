from flask import Flask, render_template
from src.routes import data_script, home

app = Flask(__name__)

app.register_blueprint(data_script.script, url_prefix='/script')
app.register_blueprint(home.home, url_prefix='/home')

# página de apresentação
@app.route('/')
def landingpage():
    return render_template('landingpage.html')
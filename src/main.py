from flask import Flask, render_template
from src.routes import data_script

app = Flask(__name__)

app.register_blueprint(data_script.script, url_prefix='script')

# página de apresentação
@app.route('/')
def home():
    return render_template('landingpage.html')
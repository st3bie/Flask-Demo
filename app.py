from flask import Flask
from markupsafe import escape
import sqlalchemy as db

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Flask Demo App</h1>"

if __name__ == '__main__':
    app.run()
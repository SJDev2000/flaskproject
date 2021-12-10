from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mysecretkey123"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Admin@localhost/flask2"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

from flaskproject import routes
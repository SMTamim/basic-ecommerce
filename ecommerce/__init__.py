from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ecommerce import db_info
import os
from flask_bcrypt import Bcrypt
from datetime import timedelta
# from flask_mysqldb import MySQL

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.getcwd()), 'ecommerce', 'static', 'uploads')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "verySecretKey"
app.permanent_session_lifetime = timedelta(days=5)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from ecommerce import routes

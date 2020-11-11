from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import timedelta
from waitress import serve

import os


app = Flask(__name__)
serve(app, host='0.0.0.0', port=8080)
application = app
app.config.from_object(Config)
app.use_reloader = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


from app import routes, models

 

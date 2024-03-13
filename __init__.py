from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config["SECRET_KEY"] = '33b3eeb5c87ea2e9d5e202d588ecbc3f'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Para Acessar Esta Pagina Faça o Login Primeiro"
login_manager.login_message_category = "alert-info"


from comunidadeimpressionadora import routes
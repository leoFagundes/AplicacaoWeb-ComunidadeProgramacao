from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config["SECRET_KEY"] = '7b64d4d261aaed111e632302ef1ac0ad'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #quando o usuário tenta entrar em uma página em que ele não está autorizado, vai direcionar ele para outra página
login_manager.login_message_category = 'alert-info' #cor amarela para alerta (bootstrap)
login_manager.login_message = 'Faça login para acessar essa página.' #mensagem que aparece


from comunidadeprogs import routes
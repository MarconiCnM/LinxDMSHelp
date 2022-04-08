from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import urllib.parse


app = Flask(__name__)

app.config['SECRET_KEY'] = '900b934668183d4effbc7e84cbad2116'

params = urllib.parse.quote_plus(
    'DRIVER={SQL Server};SERVER=MARCONI;DATABASE=LINXDMSHELP;Trusted_Connection=yes;')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'loginPage'
login_manager.login_message_category = 'alert-warning'

from routes import authRoutes
from routes import cadastrosRoutes
from routes import solicitacoesRoutes

authRoutes.init_app(app)
cadastrosRoutes.init_app(app)
solicitacoesRoutes.init_app(app)
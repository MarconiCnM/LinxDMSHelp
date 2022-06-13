from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail 
import urllib.parse


app = Flask(__name__)

app.config['SECRET_KEY'] = '900b934668183d4effbc7e84cbad2116'

params = urllib.parse.quote_plus(
    'DRIVER={SQL Server};SERVER=MTZNOTFS031063.linx-inves.com.br;DATABASE=LINXDMSHELP;Trusted_Connection=yes;')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'loginPage'
login_manager.login_message_category = 'alert-warning'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'linxdmshelp@gmail.com',
    "MAIL_PASSWORD": 'ASDFqwer1597*Linx'
}

app.config.update(mail_settings)

mail = Mail(app)

from routes import authRoutes
from routes import dashboardRoutes
from routes import cadastrosRoutes
from routes import solErroRoutes
from routes import solAlteracaoRoutes
from routes import solservicoRoutes
from routes import solCompRoutes
from routes import solImportRoutes
from routes import solShareRoutes
from routes import solHelpRoutes

authRoutes.init_app(app)
dashboardRoutes.init_app(app)
cadastrosRoutes.init_app(app)
solErroRoutes.init_app(app)
solAlteracaoRoutes.init_app(app)
solservicoRoutes.init_app(app)
solCompRoutes.init_app(app)
solImportRoutes.init_app(app)   
solShareRoutes.init_app(app)
solHelpRoutes.init_app(app)
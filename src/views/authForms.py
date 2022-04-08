from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email

class FormLogin(FlaskForm):
    email = StringField('E-mail', render_kw={"placeholder": "Digite seu e-mail..."},
                        validators=[DataRequired(), Email()])
    password = PasswordField(
        'Senha', render_kw={"placeholder": "Digite sua senha..."}, validators=[DataRequired()])
    remmember = BooleanField('Lembrar meu login')
    btn_submit_login = SubmitField('Conectar')
from flask import flash
from flask_login import login_user
from models.models import GESTOR, HELPER, ANALISTA
from app import bcrypt


def authLogin(form_login):
    if form_login.validate_on_submit():
        gestor = GESTOR.query.filter_by(EMAIL=form_login.email.data).first()
        helper = HELPER.query.filter_by(EMAIL=form_login.email.data).first()
        analista = ANALISTA.query.filter_by(EMAIL=form_login.email.data).first()

        if gestor and bcrypt.check_password_hash(gestor.SENHA, form_login.password.data):
            login_user(gestor, remember=form_login.remmember.data)
            flash('Login feito com sucesso', 'alert-success')
            return True
        elif helper and bcrypt.check_password_hash(helper.SENHA, form_login.password.data):
            login_user(helper, remember=form_login.remmember.data)
            flash('Login feito com sucesso', 'alert-success')
            return True
        elif analista and bcrypt.check_password_hash(analista.SENHA, form_login.password.data):
            login_user(analista, remember=form_login.remmember.data)
            flash('Login feito com sucesso', 'alert-success')
            return True
        else:
            flash('Falha no login. e-mail ou senha incorretos', 'alert-danger')

from flask import Flask, redirect, render_template, url_for, flash
from flask_login import login_required, current_user, logout_user

from views.authForms import FormLogin
from controllers.authController import authLogin
from models.models import BASES, GESTOR, HELPER

def init_app(app: Flask):
    @app.route("/", methods=['GET', 'POST'])
    def loginPage():
        form_login = FormLogin()
        auth = authLogin(form_login)
        if auth:
            return redirect(url_for('dashboard'))

        return render_template('index.html', form_login=form_login)

    @app.route('/dashboard', methods=['GET', 'POST'])
    @login_required
    def dashboard():
        bases_oracle = BASES.query.filter_by(ESTRUTURA='Oracle').all()
        bases_sqlserver = BASES.query.filter_by(ESTRUTURA='SQLServer').all()
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            return render_template('/main/dashboards/dashboardGestor.html', bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver)
        elif HELPER.query.filter_by(EMAIL=current_user.EMAIL).first():
            return render_template('/main/dashboards/dashboardHelper.html', bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver)
        else:
            return render_template('/main/dashboards/dashboardAnalista.html', bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver)

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Logout feito com sucesso', 'alert-success')
        return redirect(url_for('loginPage'))
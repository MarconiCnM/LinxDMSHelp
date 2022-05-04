from flask import Flask, redirect, render_template, url_for, flash
from flask_login import logout_user

from views.authForms import FormLogin
from controllers.authController import authLogin

def init_app(app: Flask):
    @app.route("/", methods=['GET', 'POST'])
    def loginPage():
        form_login = FormLogin()
        auth = authLogin(form_login)
        if auth:
            return redirect(url_for('dashboard'))

        return render_template('index.html', form_login=form_login)
    
    @app.route('/logout')
    def logout():
        logout_user()
        flash('Logout feito com sucesso', 'alert-success')
        return redirect(url_for('loginPage'))
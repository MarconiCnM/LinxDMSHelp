from flask import Flask, redirect, render_template, url_for, flash
from flask_login import login_required, current_user, logout_user
import datetime

from views.authForms import FormLogin
from controllers.authController import authLogin
from models.models import ANALISTA, BASES, GESTOR, HELPER, CONTROLE_TPS_GERAIS, CONTROLE_TPS_ANALISTAS, TIME

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
        tps_gerais = CONTROLE_TPS_GERAIS.query.first()
        tps_analistas = CONTROLE_TPS_ANALISTAS.query.filter_by(ANALISTA=str.title(current_user.EMAIL.replace(
            '.', ' ').split('@')[0])).all()
        data_hoje = datetime.datetime.today()
        bases_oracle = BASES.query.filter_by(ESTRUTURA='Oracle').all()
        bases_sqlserver = BASES.query.filter_by(ESTRUTURA='SQLServer').all()
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            time = TIME.query.filter_by(GESTOR_ID=current_user.id).first()
            analistas_gestor = []
            for analista in time.ANALISTAS:
                analistas_gestor.append(analista.USUARIO)

            tps_time = CONTROLE_TPS_ANALISTAS.query.filter(ANALISTA.USUARIO.in_(analistas_gestor)).all()
            return render_template('/main/dashboards/dashboardGestor.html', bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tps_time=tps_time, data_hoje=data_hoje)
        elif HELPER.query.filter_by(EMAIL=current_user.EMAIL).first():
            time = TIME.query.filter_by(HELPER_ID=current_user.id).first()
            analistas_help = []
            for analista in time.ANALISTAS:
                analistas_help.append(analista.USUARIO)

            tps_time = CONTROLE_TPS_ANALISTAS.query.filter(ANALISTA.USUARIO.in_(analistas_help)).all()
            return render_template('/main/dashboards/dashboardHelper.html', bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tps_time=tps_time, data_hoje=data_hoje)
        else:
            return render_template('/main/dashboards/dashboardAnalista.html', bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tps_analistas=tps_analistas, data_hoje=data_hoje)

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Logout feito com sucesso', 'alert-success')
        return redirect(url_for('loginPage'))
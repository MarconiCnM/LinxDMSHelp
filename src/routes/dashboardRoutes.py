from flask import Flask, render_template
from flask_login import login_required, current_user

from controllers.authController import tpsAnalistas, tpsTimeGestor, tpsTimeHelper, tpsTimeCoordenador
from models.models import BASES, GESTOR, HELPER, CONTROLE_TPS_GERAIS

def init_app(app: Flask):
    @app.route('/dashboard', methods=['GET', 'POST'])
    @login_required
    def dashboard():
        tps_gerais = CONTROLE_TPS_GERAIS.query.first()
        bases_oracle = BASES.query.filter_by(ESTRUTURA='Oracle').all()
        bases_sqlserver = BASES.query.filter_by(ESTRUTURA='SQLServer').all()
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                result = tpsTimeCoordenador()
                tpsanaliticotot = enumerate(result[3], start=0)
                tps_analistas = enumerate(result[0], start=1)
                tps_analistas15 = enumerate(result[1], start=1)
                tps_backlog = enumerate(result[2], start=1)
            else: 
                result = tpsTimeGestor()
                tpsanaliticotot = enumerate(result[3], start=0)
                tps_analistas = enumerate(result[0], start=1)
                tps_analistas15 = enumerate(result[1], start=1)
                tps_backlog = enumerate(result[2], start=1)
            return render_template('/main/dashboards/dashboardGestor.html', bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tpsanaliticotot=tpsanaliticotot, tps_analistas=tps_analistas, tps_analistas15=tps_analistas15, tps_backlog=tps_backlog)
        elif HELPER.query.filter_by(EMAIL=current_user.EMAIL).first():
            result = tpsTimeHelper()
            tpsanaliticotot = enumerate(result[3], start=0)
            tps_analistas = enumerate(result[0], start=1)
            tps_analistas15 = enumerate(result[1], start=1)
            tps_backlog = enumerate(result[2], start=1)

            return render_template('/main/dashboards/dashboardHelper.html', bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tpsanaliticotot=tpsanaliticotot, tps_analistas=tps_analistas, tps_analistas15=tps_analistas15, tps_backlog=tps_backlog)
        else:
            result = tpsAnalistas()
            tps_analistas = enumerate(result[0], start=1)
            tps_analistas15 = enumerate(result[1], start=1)
            tps_backlog = enumerate(result[2], start=1)
            return render_template('/main/dashboards/dashboardAnalista.html', bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tps_analistas=tps_analistas, tps_analistas15=tps_analistas15, tps_backlog=tps_backlog)

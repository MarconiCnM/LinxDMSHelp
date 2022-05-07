from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import mail, mail_settings
from flask_mail import Message

from controllers.authController import tpsAnalistas, tpsTimeGestor, tpsTimeHelper, tpsTimeCoordenador
from models.models import BASES, ANALISTA, GESTOR, HELPER, CONTROLE_TPS_GERAIS, CONTROLE_TPS_ANALISTAS

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
                tipo = 'G'
            else: 
                result = tpsTimeGestor()
                tpsanaliticotot = enumerate(result[3], start=0)
                tps_analistas = enumerate(result[0], start=1)
                tps_analistas15 = enumerate(result[1], start=1)
                tps_backlog = enumerate(result[2], start=1)
                tipo = 'G'
            return render_template('/main/dashboards/dashboardGestor.html', tipo=tipo, bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tpsanaliticotot=tpsanaliticotot, tps_analistas=tps_analistas, tps_analistas15=tps_analistas15, tps_backlog=tps_backlog)
        elif HELPER.query.filter_by(EMAIL=current_user.EMAIL).first():
            result = tpsTimeHelper()
            tpsanaliticotot = enumerate(result[3], start=0)
            tps_analistas = enumerate(result[0], start=1)
            tps_analistas15 = enumerate(result[1], start=1)
            tps_backlog = enumerate(result[2], start=1)
            tipo = 'H'
            return render_template('/main/dashboards/dashboardHelper.html', tipo=tipo, bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tpsanaliticotot=tpsanaliticotot, tps_analistas=tps_analistas, tps_analistas15=tps_analistas15, tps_backlog=tps_backlog)
        else:
            result = tpsAnalistas()
            tps_analistas = enumerate(result[0], start=1)
            tps_analistas15 = enumerate(result[1], start=1)
            tps_backlog = enumerate(result[2], start=1)
            tipo = 'A'
            return render_template('/main/dashboards/dashboardAnalista.html', tipo=tipo, bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tps_analistas=tps_analistas, tps_analistas15=tps_analistas15, tps_backlog=tps_backlog)

    @app.route("/solicitaMov/<tp_id>", methods=['GET', 'POST'])
    def solicitaMov(tp_id):
        tp = CONTROLE_TPS_ANALISTAS.query.filter_by(NRO_TP=tp_id).first()
        analista = ANALISTA.query.filter_by(USUARIO=tp.ANALISTA).first()
        print(analista.EMAIL)

        msg = Message(
                subject = 'Solicitação de movimentação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [analista.EMAIL],
                body = f'''
                Bom dia {analista.USUARIO},

                A TP {tp.NRO_TP} está a muito tempo sem movimentação, favor fazer a movimentação da mesma para que o "Fim Previsto" sejá atualizado e não conte como backlog indevidamente,

                OBS: TPs com o status "Aguardando Cliente Validar", "Aguardando Informação Externa" ou "Aguardando Desenvolvimento" quando fizermos a movimentação diária na TP, será 
                necessário utilizar a opção de "Alteração de Status", bastando selecionar o "Novo Status" igual ao anterior para atualizar o campo "Fim Previsto".

                Qualquer problema ou duvida não hesite em acionar seu Helper, 

                Atenciosamente,
                Suporte Help
                '''
            )

        mail.send(msg)


        flash('E-email enviado', 'alert-success')
        
        return redirect(url_for('dashboard'))

    @app.route("/solicitaInf/<tp_id>", methods=['GET', 'POST'])
    def solicitaInf(tp_id):
        tp = CONTROLE_TPS_ANALISTAS.query.filter_by(NRO_TP=tp_id).first()
        analista = ANALISTA.query.filter_by(USUARIO=tp.ANALISTA).first()
        print(analista.EMAIL)

        msg = Message(
                subject = 'Solicitação de Informação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [analista.EMAIL],
                body = f'''
                Bom dia {analista.USUARIO},

                {current_user.USUARIO} solicita um email detalhado de como esta a atual situação da tp {tp.NRO_TP}, preencha os campos abaixo e o envie para o email {current_user.EMAIL}.

                Solicitação/Reclamação do cliente:
                O que ja foi analisado:
                Esta aguardando alguem? Se sim descreva quem o por que:
                Manuais validados:
                Analistas acionados:
                Estrutura do cliente:
                Versão do cliente:
                Ele está atualizado: 

                OBS: Se existir algum anexo na tp envie em anexo no email.

                Qualquer problema ou duvida não hesite em acionar seu Helper, 

                Atenciosamente,
                Suporte Help
                '''
            )

        mail.send(msg)


        flash('E-email enviado', 'alert-success')
        
        return redirect(url_for('dashboard'))
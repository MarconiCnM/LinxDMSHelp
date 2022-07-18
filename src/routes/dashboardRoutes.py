from posixpath import dirname
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from app import mail, mail_settings
from flask_mail import Message
import pandas as pd
from datetime import datetime
import os

from controllers.dashboardController import contSolGestor, tpsAnalistas, tpsTimeGestor, tpsTimeHelper, tpsTimeCoordenador, contSolAnalista, contSolHelper, contSolCoordenador, pegaLink
from models.models import BASES, ANALISTA, GESTOR, HELPER, CONTROLE_TPS_GERAIS, CONTROLE_TPS_ANALISTAS
from views.ferramentaForms import FormCriaAtualiza

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
                cont_sol = contSolCoordenador()
                tpsanaliticotot = enumerate(result[3], start=0)
                tps_analistas = enumerate(result[0], start=1)
                tps_analistas15 = enumerate(result[1], start=1)
                tps_backlog = enumerate(result[2], start=1)
                tipo = 'G'
            else: 
                result = tpsTimeGestor()
                cont_sol = contSolGestor()
                tpsanaliticotot = enumerate(result[3], start=0)
                tps_analistas = enumerate(result[0], start=1)
                tps_analistas15 = enumerate(result[1], start=1)
                tps_backlog = enumerate(result[2], start=1)
                tipo = 'G'
            return render_template('/main/dashboards/dashboardGestor.html', tipo=tipo, bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tpsanaliticotot=tpsanaliticotot, tps_analistas=tps_analistas, tps_analistas15=tps_analistas15, tps_backlog=tps_backlog, cont_sol=cont_sol)
        elif HELPER.query.filter_by(EMAIL=current_user.EMAIL).first():
            result = tpsTimeHelper()
            cont_sol = contSolHelper()
            tpsanaliticotot = enumerate(result[3], start=0)
            tps_analistas = enumerate(result[0], start=1)
            tps_analistas15 = enumerate(result[1], start=1)
            tps_backlog = enumerate(result[2], start=1)
            tipo = 'H'
            return render_template('/main/dashboards/dashboardHelper.html', tipo=tipo, bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tpsanaliticotot=tpsanaliticotot, tps_analistas=tps_analistas, tps_analistas15=tps_analistas15, tps_backlog=tps_backlog, cont_sol=cont_sol)
        else:
            result = tpsAnalistas()
            cont_sol = contSolAnalista()
            tps_analistas = enumerate(result[0], start=1)
            tps_analistas15 = enumerate(result[1], start=1)
            tps_backlog = enumerate(result[2], start=1)
            tipo = 'A'
            return render_template('/main/dashboards/dashboardAnalista.html', tipo=tipo, bases_oracle=bases_oracle, bases_sqlserver=bases_sqlserver, tps_gerais=tps_gerais, tps_analistas=tps_analistas, tps_analistas15=tps_analistas15, tps_backlog=tps_backlog, cont_sol=cont_sol)

    @app.route("/solicitaMov/<tp_id>", methods=['GET', 'POST'])
    @login_required
    def solicitaMov(tp_id):
        tp = CONTROLE_TPS_ANALISTAS.query.filter_by(NRO_TP=tp_id).first()
        analista = ANALISTA.query.filter_by(USUARIO=tp.ANALISTA).first()

        msg = Message(
                subject = 'Solicitação de movimentação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [analista.EMAIL],
                body = f'''Bom dia {analista.USUARIO},

A TP {tp.NRO_TP} está a muito tempo sem movimentação, favor fazer a movimentação da mesma para que o "Fim Previsto" sejá atualizado e não conte como backlog indevidamente,

OBS: TPs com o status "Aguardando Cliente Validar", "Aguardando Informação Externa" ou "Aguardando Desenvolvimento" quando fizermos a movimentação diária na TP, será 
necessário utilizar a opção de "Alteração de Status", bastando selecionar o "Novo Status" igual ao anterior para atualizar o campo "Fim Previsto".

Qualquer problema ou duvida não hesite em acionar seu Helper, 

Atenciosamente,
Suporte Help
                '''
            )

        #mail.send(msg)

        flash('E-email enviado', 'alert-success')
        
        return redirect(url_for('dashboard'))

    @app.route("/solicitaInf/<tp_id>", methods=['GET', 'POST'])
    @login_required
    def solicitaInf(tp_id):
        tp = CONTROLE_TPS_ANALISTAS.query.filter_by(NRO_TP=tp_id).first()
        analista = ANALISTA.query.filter_by(USUARIO=tp.ANALISTA).first()

        msg = Message(
                subject = 'Solicitação de Informação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [analista.EMAIL],
                body = f'''Bom dia {analista.USUARIO},

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

        #mail.send(msg)


        flash('E-email enviado', 'alert-success')
        
        return redirect(url_for('dashboard'))


    @app.route("/expgeral", methods=['GET', 'POST'])
    @login_required
    def expgeral():
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                result = tpsTimeCoordenador()
            else: 
                result = tpsTimeGestor()
        elif HELPER.query.filter_by(EMAIL=current_user.EMAIL).first():
            result = tpsTimeHelper()

        tps_analistas = result[0]
        marks_data  = pd.DataFrame(
            tps_analistas
        )

        name = 'Inf_tps_geral' + datetime.today().strftime('%d-%m-%Y') + '.xlsx'
        dir_name = os.path.join(
                app.root_path, 'static', 'exp/')
  
        marks_data.to_excel(dir_name + name)

        flash('Exportação realizada com sucesso', 'alert-success')

        return send_from_directory(dir_name, name, as_attachment=True)

    @app.route("/expissues", methods=['GET', 'POST'])
    @login_required
    def expissues():
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                result = tpsTimeCoordenador()
            else: 
                result = tpsTimeGestor()
        elif HELPER.query.filter_by(EMAIL=current_user.EMAIL).first():
            result = tpsTimeHelper()

        tps_analistas = result[4]
        marks_data  = pd.DataFrame(
            tps_analistas
        )

        name = 'Inf_tps_issue' + datetime.today().strftime('%d-%m-%Y') + '.xlsx'
        dir_name = os.path.join(
                app.root_path, 'static', 'exp/')
  
        marks_data.to_excel(dir_name + name)

        flash('Exportação realizada com sucesso', 'alert-success')

        return send_from_directory(dir_name, name, as_attachment=True)

    @app.route("/expmais15", methods=['GET', 'POST'])
    @login_required
    def expmais15():
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                result = tpsTimeCoordenador()
            else: 
                result = tpsTimeGestor()
        elif HELPER.query.filter_by(EMAIL=current_user.EMAIL).first():
            result = tpsTimeHelper()

        tps_analistas = result[1]
        marks_data  = pd.DataFrame(
            tps_analistas
        )

        name = 'Inf_tps_mais15' + datetime.today().strftime('%d-%m-%Y') + '.xlsx'
        dir_name = os.path.join(
                app.root_path, 'static', 'exp/')
  
        marks_data.to_excel(dir_name + name)

        flash('Exportação realizada com sucesso', 'alert-success')

        return send_from_directory(dir_name, name, as_attachment=True)

    @app.route("/expbacklogs", methods=['GET', 'POST'])
    @login_required
    def expbacklogs():
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                result = tpsTimeCoordenador()
            else: 
                result = tpsTimeGestor()
        elif HELPER.query.filter_by(EMAIL=current_user.EMAIL).first():
            result = tpsTimeHelper()
        tps_analistas = result[2]
        marks_data  = pd.DataFrame(
            tps_analistas
        )

        name = 'Inf_tps_backlogs' + datetime.today().strftime('%d-%m-%Y') + '.xlsx'
        dir_name = os.path.join(
                app.root_path, 'static', 'exp/')
  
        marks_data.to_excel(dir_name + name)

        flash('Exportação realizada com sucesso', 'alert-success')

        return send_from_directory(dir_name, name, as_attachment=True)

    @app.route("/limpezatemporarios", methods=['GET', 'POST'])
    @login_required
    def limpezatemp():
        name = 'script-limpeza' + '.bat'
        dir_name = os.path.join(
                app.root_path, 'static', 'exp/')

        return send_from_directory(dir_name, name, as_attachment=True)
    

    @app.route('/criaatualiza', methods=['GET', 'POST'])
    @login_required
    def criaatualiza():
        form_atualizacria = FormCriaAtualiza()

        if form_atualizacria.validate_on_submit() and 'btn_submit_criar' in request.form and request.method == 'POST':
            if form_atualizacria.diretorio.data == '':
                flash('Por favor preencha o diretorio', 'alert-danger')
            else:
                links = pegaLink(form_atualizacria)
                dir = form_atualizacria.diretorio.data

                if form_atualizacria.estrutura.data == '2 Camadas':
                    modelo = 'https://distribuicao.blob.core.windows.net/suporte/Marconi/Modelo.zip'
                    texto = f"""@echo off
set PATH=%PATH%;C:/Program Files/7-Zip/
mkdir "{dir}"
cd "{dir}"
cUrl.exe "{modelo}" -o "{dir}\Modelo.zip"

7z e -y "Modelo.zip"
xcopy "{dir}\Modelo\." "{dir}" /e

rmdir Modelo /s /q

cUrl.exe "{links[0]}" -o "{dir}\{links[0].split('/')[-1]}"
cUrl.exe "{links[1]}" -o "{dir}\{links[1].split('/')[-1]}"
cUrl.exe "{links[2]}" -o "{dir}\{links[2].split('/')[-1]}"

7z e -y "{links[0].split('/')[-1]}"
7z e -y "{links[1].split('/')[-1]}"
7z e -y "{links[2].split('/')[-1]}" 

del {links[0].split('/')[-1]}
del {links[1].split('/')[-1]}
del {links[2].split('/')[-1]}
"""
                elif form_atualizacria.estrutura.data == '3 Camadas':
                    modelo = 'https://distribuicao.blob.core.windows.net/suporte/Marconi/Modelo-3Camadas.zip'
                    texto = f"""@echo off
set PATH=%PATH%;C:/Program Files/7-Zip/
mkdir "{dir}"
cd "{dir}"
cUrl.exe "{modelo}" -o "{dir}\Modelo.zip"

7z e "Modelo.zip"
xcopy "{dir}\Modelo-3Camadas\." "{dir}" /e

rmdir Modelo-3Camadas /s /q

cUrl.exe "{links[0]}" -o "{dir}\{links[0].split('/')[-1]}"
cUrl.exe "{links[1]}" -o "{dir}\{links[1].split('/')[-1]}"
cUrl.exe "{links[2]}" -o "{dir}\{links[2].split('/')[-1]}"
cUrl.exe "{links[3]}" -o "{dir}\{links[3].split('/')[-1]}"
cUrl.exe "{links[4]}" -o "{dir}\{links[4].split('/')[-1]}"

7z e -y "{links[0].split('/')[-1]}"
7z e -y "{links[1].split('/')[-1]}"
7z e -y "{links[2].split('/')[-1]}" 
7z e -y "{links[3].split('/')[-1]}" 
7z e -y "{links[4].split('/')[-1]}" 

del {links[0].split('/')[-1]}
del {links[1].split('/')[-1]}
del {links[2].split('/')[-1]}
del {links[3].split('/')[-1]}
del {links[4].split('/')[-1]}

    """
                name = 'criasistema-' + datetime.today().strftime('%d-%m-%Y') + '.bat'
                dir_name = os.path.join(
                        app.root_path, 'static', 'exp\\')
        
                arquivo = open(dir_name + name, 'w') 
                arquivo.write(texto)
                arquivo.close()

                flash('Exportação realizada com sucesso', 'alert-success')

                return send_from_directory(dir_name, name, as_attachment=True)

        if form_atualizacria.validate_on_submit() and 'btn_submit_atualizar' in request.form and request.method == 'POST':
            if form_atualizacria.diretorioatualiza.data == '':
                flash('Por favor preencha o diretorio', 'alert-danger')
            else:
                links = pegaLink(form_atualizacria)
                dir = form_atualizacria.diretorioatualiza.data

                if form_atualizacria.estrutura.data == '2 Camadas':
                    texto = f"""@echo off
set PATH=%PATH%;C:/Program Files/7-Zip/
cd "{dir}"

cUrl.exe "{links[1]}" -o "{dir}\{links[1].split('/')[-1]}"

7z e -y "{links[1].split('/')[-1]}"

del {links[1].split('/')[-1]}
"""
                elif form_atualizacria.estrutura.data == '3 Camadas':
                    texto = f"""@echo off
set PATH=%PATH%;C:/Program Files/7-Zip/
cd "{dir}"

cUrl.exe "{links[2]}" -o "{dir}\{links[2].split('/')[-1]}"
cUrl.exe "{links[3]}" -o "{dir}\{links[3].split('/')[-1]}"

7z e -y "{links[2].split('/')[-1]}" 
7z e -y "{links[3].split('/')[-1]}" 

del {links[2].split('/')[-1]}
del {links[3].split('/')[-1]}

    """

                name = 'atualizasistema-' + datetime.today().strftime('%d-%m-%Y') + '.bat'
                dir_name = os.path.join(
                        app.root_path, 'static', 'exp\\')
        
                arquivo = open(dir_name + name, 'w') 
                arquivo.write(texto)
                arquivo.close()

                flash('Exportação realizada com sucesso', 'alert-success')

                return send_from_directory(dir_name, name, as_attachment=True)


        return render_template('/main/ferramentas/criaatualiza.html', form_atualizacria=form_atualizacria)

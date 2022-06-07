import os
from datetime import datetime, timedelta
from flask import request, flash
from flask_login import current_user
from flask_mail import Message

from models.models import SOL_SCRIPT, MOV_SOL, TIME, HELPER, ANALISTA
from app import app, database, mail, mail_settings

def solComp(form_comp):
    if form_comp.validate_on_submit() and 'btn_submit_inserir' in request.form:
        comp = SOL_SCRIPT.query.filter_by(
            NRO_TP=form_comp.nro_tp.data).first()

        if comp:
            flash(
                'Já existe solicitação de analise de comp para essa TP', 'alert-danger')
        elif form_comp.script.data is None:
            flash(
                'Por favor adicione os arquivos', 'alert-danger')
        else:
            time = TIME.query.filter_by(id=current_user.TIME_ID).first()
            helper = HELPER.query.filter_by(id=time.HELPER_ID).first()

            name, extension = os.path.splitext(form_comp.script.data.filename)
            name = str(form_comp.nro_tp.data) + '-' + \
                datetime.today().strftime('%d-%m-%Y.%H:%M')
            complete_name = name + extension
            complete_path = os.path.join(
                app.root_path, 'static', 'docs', 'script', complete_name)
            form_comp.script.data.save(complete_path)

            comp = SOL_SCRIPT(NRO_TP=form_comp.nro_tp.data, GRUPO=form_comp.grupo.data, OQUE=form_comp.oque.data, 
                            PORQUE=form_comp.porque.data, SCRIPT=complete_name, ANALISTA_ID=current_user.id, HELPER_ID=helper.id)
            database.session.add(comp)

            mov = MOV_SOL(NRO_TP=form_comp.nro_tp.data, TITULO='Abertura de Analise', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO='Solicitação de compilação aberta', STATUS='AGUARDANDO INICIALIZAÇÂO')
            database.session.add(mov)
            database.session.commit()

            enviaEmailComp(comp.NRO_TP, 'I')

            flash('Solicitação feita com sucesso', 'alert-success')

            return True
    
    if form_comp.validate_on_submit() and 'btn_submit_iniciar' in request.form:
        comp = SOL_SCRIPT.query.filter_by(
            NRO_TP=form_comp.nro_tp.data).first()

        comp.NRO_TP=form_comp.nro_tp.data 
        comp.ISSUE=form_comp.issue.data
        comp.GRUPO=form_comp.grupo.data              
        comp.OQUE=form_comp.oque.data 
        comp.PORQUE=form_comp.porque.data
        comp.SOLUCAO=form_comp.solucao.data
        comp.HELPER_ID=current_user.id
        comp.STATUS = 'EM ANALISE'

        mov = MOV_SOL(NRO_TP=form_comp.nro_tp.data, TITULO='Analise Iniciada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Mov', STATUS='EM ANALISE')
        database.session.add(mov)
        database.session.commit()

        enviaEmailComp(comp.NRO_TP, 'H')

        flash('Analise Iniciada', 'alert-success')
        return True
    
    if form_comp.validate_on_submit() and 'btn_submit_aprov' in request.form:
        comp = SOL_SCRIPT.query.filter_by(
            NRO_TP=form_comp.nro_tp.data).first()

        if form_comp.issue.data == '':
            flash(
                'Por favor informe o numero da issue aberta', 'alert-danger')
        else:
            comp.NRO_TP=form_comp.nro_tp.data 
            comp.ISSUE=form_comp.issue.data
            comp.GRUPO=form_comp.grupo.data              
            comp.OQUE=form_comp.oque.data 
            comp.PORQUE=form_comp.porque.data
            comp.SOLUCAO=form_comp.solucao.data
            comp.STATUS = 'AGUARDANDO COMPILAÇÃO'

            mov = MOV_SOL(NRO_TP=form_comp.nro_tp.data, TITULO='Aprovação de Abertura de ISSUE', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação aprovada, aguardando compilação da distribuição', STATUS='AGUARDANDO COMPILAÇÃO')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailComp(comp.NRO_TP, 'H')
            
            flash('Aprovada, aguardando compilação', 'alert-success')
            
            return True
    
    if form_comp.validate_on_submit() and 'btn_submit_final' in request.form:
        comp = SOL_SCRIPT.query.filter_by(
            NRO_TP=form_comp.nro_tp.data).first()
        
        if form_comp.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            comp.NRO_TP=form_comp.nro_tp.data 
            comp.ISSUE=form_comp.issue.data
            comp.GRUPO=form_comp.grupo.data              
            comp.OQUE=form_comp.oque.data 
            comp.PORQUE=form_comp.porque.data
            comp.SOLUCAO=form_comp.solucao.data
            comp.DTA_CONCLUDED = datetime.utcnow()
            comp.STATUS='FINALIZADA'

            mov = MOV_SOL(NRO_TP=form_comp.nro_tp.data, TITULO='Solicitação Finalizada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Compilação feita e analise finalizada', STATUS='FINALIZADA')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailComp(comp.NRO_TP, 'H')

            flash('Solicitação Finalizada', 'alert-success')

            return True
    if form_comp.validate_on_submit() and 'btn_submit_recus' in request.form:
        comp = SOL_SCRIPT.query.filter_by(
            NRO_TP=form_comp.nro_tp.data).first()
        
        if form_comp.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            comp.NRO_TP=form_comp.nro_tp.data 
            comp.ISSUE=form_comp.issue.data
            comp.GRUPO=form_comp.grupo.data              
            comp.OQUE=form_comp.oque.data 
            comp.PORQUE=form_comp.porque.data
            comp.SOLUCAO=form_comp.solucao.data
            comp.DTA_CONCLUDED = datetime.utcnow()
            comp.STATUS='NÃO APROVADO'

            mov = MOV_SOL(NRO_TP=form_comp.nro_tp.data, TITULO='Solicitação Recusada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação não aprovada', STATUS='NÃO APROVADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailComp(comp.NRO_TP, 'H')

            flash('Solicitação Recusada', 'alert-success')

            return True 
    if form_comp.validate_on_submit() and 'btn_submit_encaminhar' in request.form:
        comp = SOL_SCRIPT.query.filter_by(
            NRO_TP=form_comp.nro_tp.data).first()
        
        if comp:
            helper = HELPER.query.filter_by(USUARIO=form_comp.helper.data).first()

            comp.HELPER_ID=helper.id
            comp.STATUS='NÃO INICIADO'

            mov = MOV_SOL(NRO_TP=form_comp.nro_tp.data, TITULO='Solicitação Encaminhada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação teve seu helper trocado', STATUS='NÃO INICIADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailComp(comp.NRO_TP, 'I')

            flash('Solicitação Encaminhada', 'alert-success')

            return True         




def solCompTime():
    result = SOL_SCRIPT.query.filter_by(HELPER_ID=current_user.id)

    return result

def solCompTimeGestor():
    result = SOL_SCRIPT.query.filter().join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id)))

    return result

def solCompTimeCoordenador():
    result = SOL_SCRIPT.query.filter().all()

    return result


def enviaEmailComp(tp_id, tipo):
    if tipo == 'H':
        scriptID = SOL_SCRIPT.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Solicitação de Informação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [scriptID.requester.EMAIL],
                body = f'''
                Bom dia {scriptID.requester.USUARIO},

                A solicitação de analise de compilação sobre a TP {scriptID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'A':
        scriptID = SOL_SCRIPT.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Notificação de Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [scriptID.finisher.EMAIL],
                body = f'''
                Bom dia {scriptID.finisher.USUARIO},

                A solicitação de analise de compilação sobre a TP {scriptID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'I':
        scriptID = SOL_SCRIPT.query.filter_by(NRO_TP=tp_id).first()
        helper = HELPER.query.filter_by(id=scriptID.HELPER_ID).first()

        msg = Message(
                subject = 'Nova Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [helper.EMAIL],
                body = f'''
                Bom dia {helper.USUARIO},

                Foi criada uma solicitação de analise de compilação sobre a TP {scriptID.NRO_TP},

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    else:
        flash('Erro', 'danger-success')

    return True

def formatDate(dta_create):
    fuso_horario = timedelta(hours=3)
    d1 = dta_create - fuso_horario
    dataFormatada = d1.strftime('%d/%m/%Y')

    return dataFormatada

def formatDateTime(dta_create):
    fuso_horario = timedelta(hours=3)
    d1 = dta_create - fuso_horario
    dataFormatada = d1.strftime('%d/%m/%Y %H:%M')

    return dataFormatada
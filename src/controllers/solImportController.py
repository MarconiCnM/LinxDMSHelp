import os
from datetime import datetime, timedelta
from flask import request, flash
from flask_login import current_user
from flask_mail import Message

from models.models import SOL_IMPORT, MOV_SOL, TIME, HELPER, ANALISTA
from app import app, database, mail, mail_settings


def solImport(form_imp):
    if form_imp.validate_on_submit() and 'btn_submit_inserir' in request.form:
        imp = SOL_IMPORT.query.filter_by(
            NRO_TP=form_imp.nro_tp.data).first()

        if imp:
            flash(
                'Já existe solicitação de analise de importação para essa TP', 'alert-danger')
        else:
            time = TIME.query.filter_by(id=current_user.TIME_ID).first()
            helper = HELPER.query.filter_by(id=time.HELPER_ID).first()

            imp = SOL_IMPORT(NRO_TP=form_imp.nro_tp.data, GRUPO=form_imp.grupo.data, SERVIDOR=form_imp.servidor.data,
                            ISSUE=form_imp.issue.data, SCHEMA=form_imp.schema.data,TAMANHO=form_imp.tamanho.data,
                            DIR_ARQ=form_imp.link.data, OBS=form_imp.observacao.data, 
                            SOLUCAO=form_imp.solucao.data, ANALISTA_ID=current_user.id, HELPER_ID=helper.id)

            database.session.add(imp)

            mov = MOV_SOL(NRO_TP=form_imp.nro_tp.data, TITULO='Abertura de Analise', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO='Solicitação de importação aberta', STATUS='AGUARDANDO INICIALIZAÇÂO')
            database.session.add(mov)
            database.session.commit()

            enviaEmailImp(imp.NRO_TP, 'I')

            flash('Solicitação feita com sucesso', 'alert-success')

            return True

    
    if form_imp.validate_on_submit() and 'btn_submit_iniciar' in request.form:
        imp = SOL_IMPORT.query.filter_by(
            NRO_TP=form_imp.nro_tp.data).first()

        imp.NRO_TP=form_imp.nro_tp.data 
        imp.ISSUE=form_imp.issue.data
        imp.GRUPO=form_imp.grupo.data
        imp.SCHEMA=form_imp.schema.data
        imp.TAMANHO=form_imp.tamanho.data
        imp.SERVIDOR=form_imp.servidor.data
        imp.DIR_ARK=form_imp.link.data
        imp.SOLUCAO=form_imp.solucao.data
        imp.HELPER_ID=current_user.id
        imp.STATUS = 'EM IMPORTAÇÃO'

        mov = MOV_SOL(NRO_TP=form_imp.nro_tp.data, TITULO='Importação Iniciada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Mov', STATUS='EM IMPORTAÇÃO')
        database.session.add(mov)
        database.session.commit()

        enviaEmailImp(imp.NRO_TP, 'H')

        flash('Analise Iniciada', 'alert-success')
        return True

    if form_imp.validate_on_submit() and 'btn_submit_info' in request.form:
        imp = SOL_IMPORT.query.filter_by(
            NRO_TP=form_imp.nro_tp.data).first()

        
        if form_imp.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua duvida ou requisição', 'alert-danger')
        else:
            imp.NRO_TP=form_imp.nro_tp.data 
            imp.ISSUE=form_imp.issue.data
            imp.GRUPO=form_imp.grupo.data
            imp.SCHEMA=form_imp.schema.data
            imp.TAMANHO=form_imp.tamanho.data
            imp.SERVIDOR=form_imp.servidor.data
            imp.DIR_ARK=form_imp.link.data
            imp.SOLUCAO=form_imp.solucao.data
            imp.STATUS = 'AGUARDANDO INFORMAÇÃO'

            mov = MOV_SOL(NRO_TP=form_imp.nro_tp.data, TITULO='Solicitação de Informação', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO=form_imp.solucao.data, STATUS='AGUARDANDO INFORMAÇÃO')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailImp(imp.NRO_TP, 'H')

            flash('Aguardando Informação', 'alert-success')
            
            return True

    if form_imp.validate_on_submit() and 'btn_submit_infores' in request.form:
        imp = SOL_IMPORT.query.filter_by(
            NRO_TP=form_imp.nro_tp.data).first()

        
        if form_imp.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua resposta', 'alert-danger')
        else:
            imp.NRO_TP=form_imp.nro_tp.data 
            imp.ISSUE=form_imp.issue.data
            imp.GRUPO=form_imp.grupo.data
            imp.SCHEMA=form_imp.schema.data
            imp.TAMANHO=form_imp.tamanho.data
            imp.SERVIDOR=form_imp.servidor.data
            imp.DIR_ARK=form_imp.link.data
            imp.SOLUCAO=form_imp.solucao.data
            imp.STATUS = 'NÃO INICIADO'

            mov = MOV_SOL(NRO_TP=form_imp.nro_tp.data, TITULO='Conclusão de Informação', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO=form_imp.solucao.data, STATUS='EM ANALISE')
            
            database.session.add(mov)
            database.session.commit()   
            
            enviaEmailImp(imp.NRO_TP, 'A')
            
            flash('Enviada a Analise', 'alert-success')

            return True

    if form_imp.validate_on_submit() and 'btn_submit_final' in request.form:
        imp = SOL_IMPORT.query.filter_by(
            NRO_TP=form_imp.nro_tp.data).first()
        
        if form_imp.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            imp.NRO_TP=form_imp.nro_tp.data 
            imp.ISSUE=form_imp.issue.data
            imp.GRUPO=form_imp.grupo.data
            imp.SCHEMA=form_imp.schema.data
            imp.TAMANHO=form_imp.tamanho.data
            imp.SERVIDOR=form_imp.servidor.data
            imp.DIR_ARK=form_imp.link.data
            imp.SOLUCAO=form_imp.solucao.data
            imp.DTA_CONCLUDED = datetime.utcnow()
            imp.STATUS='FINALIZADA'

            mov = MOV_SOL(NRO_TP=form_imp.nro_tp.data, TITULO='Importação Finalizada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Importação finalizada', STATUS='FINALIZADA')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailImp(imp.NRO_TP, 'H')

            flash('Solicitação Finalizada', 'alert-success')

            return True
    
    if form_imp.validate_on_submit() and 'btn_submit_encaminhar' in request.form:
        imp = SOL_IMPORT.query.filter_by(
            NRO_TP=form_imp.nro_tp.data).first()
        
        if imp:
            helper = HELPER.query.filter_by(USUARIO=form_imp.helper.data).first()

            imp.HELPER_ID=helper.id
            imp.STATUS='NÃO INICIADO'

            mov = MOV_SOL(NRO_TP=form_imp.nro_tp.data, TITULO='Solicitação Encaminhada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação teve seu helper trocado', STATUS='NÃO INICIADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailImp(imp.NRO_TP, 'I')

            flash('Solicitação Encaminhada', 'alert-success')

            return True         



def solImportTime():
    result = SOL_IMPORT.query.filter_by(HELPER_ID=current_user.id)

    return result

def solImportTimeGestor():
    result = SOL_IMPORT.query.filter().join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id)))

    return result

def solImportTimeCoordenador():
    result = SOL_IMPORT.query.filter().all()

    return result

def enviaEmailImp(tp_id, tipo):
    if tipo == 'H':
        impID = SOL_IMPORT.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Solicitação de Informação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [impID.requester.EMAIL],
                body = f'''
                Bom dia {impID.requester.USUARIO},

                A solicitação de analise de serviço sobre a TP {impID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'A':
        impID = SOL_IMPORT.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Notificação de Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [impID.finisher.EMAIL],
                body = f'''
                Bom dia {impID.finisher.USUARIO},

                A solicitação de analise de serviço sobre a TP {impID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'I':
        impID = SOL_IMPORT.query.filter_by(NRO_TP=tp_id).first()
        helper = HELPER.query.filter_by(id=impID.HELPER_ID).first()

        msg = Message(
                subject = 'Nova Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [helper.EMAIL],
                body = f'''
                Bom dia {helper.USUARIO},

                Foi criada uma solicitação de analise de serviço sobre a TP {impID.NRO_TP},

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
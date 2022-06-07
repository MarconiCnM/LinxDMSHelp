import os
from datetime import datetime, timedelta
from flask import request, flash
from flask_login import current_user
from flask_mail import Message

from models.models import HELP, MOV_SOL, TIME, HELPER, ANALISTA
from app import app, database, mail, mail_settings

def solHelp(form_help):
    if form_help.validate_on_submit() and 'btn_submit_inserir' in request.form:
        help = HELP.query.filter_by(
            NRO_TP=form_help.nro_tp.data).first()

        if help:
            flash(
                'Já existe solicitação de analise de help para essa TP', 'alert-danger')
        elif form_help.docs.data is None:
            flash(
                'Por favor adicione os arquivos', 'alert-danger')
        else:
            time = TIME.query.filter_by(id=current_user.TIME_ID).first()
            helper = HELPER.query.filter_by(id=time.HELPER_ID).first()

            name, extension = os.path.splitext(
                form_help.docs.data.filename)
            name = str(form_help.nro_tp.data) + '-' + \
                datetime.today().strftime('%d-%m-%Y.%H:%M')
            complete_name = name + extension
            complete_path = os.path.join(
                app.root_path, 'static', 'docs', 'help', complete_name)
            form_help.docs.data.save(complete_path)

            help = HELP(NRO_TP=form_help.nro_tp.data, CAMINHO_MENU=form_help.menu_dir.data, 
                        CODIGO_MENU=form_help.menu_cod.data, PROBLEMA=form_help.problema.data, ANALISADO=form_help.analisado.data, 
                        PALIATIVA=form_help.paliativa.data, DUVIDA=form_help.duvida.data, DOCS=complete_name, BANCO=form_help.db_teste.data, 
                        VERSAO=form_help.versao.data, ANALISTA_ID=current_user.id, HELPER_ID=helper.id)
            database.session.add(help)

            mov = MOV_SOL(NRO_TP=form_help.nro_tp.data, TITULO='Abertura de Help', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO='Solicitação de help aberta', STATUS='AGUARDANDO INICIALIZAÇÂO')
            database.session.add(mov)
            database.session.commit()

            enviaEmailHelp(help.NRO_TP, 'I')

            flash('Solicitação feita com sucesso', 'alert-success')

            return True
    
    if form_help.validate_on_submit() and 'btn_submit_iniciar' in request.form:
        help = HELP.query.filter_by(
            NRO_TP=form_help.nro_tp.data).first()

        help.NRO_TP=form_help.nro_tp.data 
        help.CAMINHO_MENU=form_help.menu_dir.data              
        help.CODIGO_MENU=form_help.menu_cod.data 
        help.PROBLEMA=form_help.problema.data
        help.ANALISADO=form_help.analisado.data
        help.DUVIDA=form_help.duvida.data
        help.PALIATIVA=form_help.paliativa.data
        help.BANCO=form_help.db_teste.data
        help.VERSAO=form_help.versao.data
        help.SOLUCAO=form_help.solucao.data
        help.HELPER_ID=current_user.id
        help.STATUS = 'EM ANALISE'

        mov = MOV_SOL(NRO_TP=form_help.nro_tp.data, TITULO='Analise Iniciada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Mov', STATUS='EM ANALISE')
        database.session.add(mov)
        database.session.commit()

        enviaEmailHelp(help.NRO_TP, 'H')

        flash('Analise Iniciada', 'alert-success')
        return True

    if form_help.validate_on_submit() and 'btn_submit_info' in request.form:
        help = HELP.query.filter_by(
            NRO_TP=form_help.nro_tp.data).first()

        
        if form_help.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua duvida ou requisição', 'alert-danger')
        else:
            help.NRO_TP=form_help.nro_tp.data 
            help.CAMINHO_MENU=form_help.menu_dir.data              
            help.CODIGO_MENU=form_help.menu_cod.data 
            help.PROBLEMA=form_help.problema.data
            help.ANALISADO=form_help.analisado.data
            help.DUVIDA=form_help.duvida.data
            help.PALIATIVA=form_help.paliativa.data
            help.BANCO=form_help.db_teste.data
            help.VERSAO=form_help.versao.data
            help.STATUS = 'AGUARDANDO INFORMAÇÃO'

            mov = MOV_SOL(NRO_TP=form_help.nro_tp.data, TITULO='Solicitação de Informação', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO=form_help.solucao.data, STATUS='AGUARDANDO INFORMAÇÃO')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailHelp(help.NRO_TP, 'H')

            flash('Aguardando Informação', 'alert-success')
            
            return True

    if form_help.validate_on_submit() and 'btn_submit_infores' in request.form:
        help = HELP.query.filter_by(
            NRO_TP=form_help.nro_tp.data).first()

        
        if form_help.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua resposta', 'alert-danger')
        else:
            help.NRO_TP=form_help.nro_tp.data 
            help.CAMINHO_MENU=form_help.menu_dir.data              
            help.CODIGO_MENU=form_help.menu_cod.data 
            help.PROBLEMA=form_help.problema.data
            help.ANALISADO=form_help.analisado.data
            help.DUVIDA=form_help.duvida.data
            help.PALIATIVA=form_help.paliativa.data
            help.BANCO=form_help.db_teste.data
            help.VERSAO=form_help.versao.data
            help.STATUS = 'EM ANALISE'

            mov = MOV_SOL(NRO_TP=form_help.nro_tp.data, TITULO='Conclusão de Informação', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO=form_help.solucao.data, STATUS='EM ANALISE')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailHelp(help.NRO_TP, 'A')
            
            flash('Enviada a Analise', 'alert-success')

            return True

    if form_help.validate_on_submit() and 'btn_submit_aprov' in request.form:
        help = HELP.query.filter_by(
            NRO_TP=form_help.nro_tp.data).first()
        
        if form_help.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            help.NRO_TP=form_help.nro_tp.data 
            help.CAMINHO_MENU=form_help.menu_dir.data              
            help.CODIGO_MENU=form_help.menu_cod.data 
            help.PROBLEMA=form_help.problema.data
            help.ANALISADO=form_help.analisado.data
            help.DUVIDA=form_help.duvida.data
            help.PALIATIVA=form_help.paliativa.data
            help.BANCO=form_help.db_teste.data
            help.VERSAO=form_help.versao.data
            help.SOLUCAO=form_help.solucao.data
            help.DTA_CONCLUDED = datetime.utcnow()
            help.STATUS='FINALIZADA'

            mov = MOV_SOL(NRO_TP=form_help.nro_tp.data, TITULO='Solicitação Finalizada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação finalizada', STATUS='FINALIZADA')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailHelp(help.NRO_TP, 'H')

            flash('Solicitação Finalizada', 'alert-success')

            return True
    if form_help.validate_on_submit() and 'btn_submit_recus' in request.form:
        help = HELP.query.filter_by(
            NRO_TP=form_help.nro_tp.data).first()
        
        if form_help.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            help.NRO_TP=form_help.nro_tp.data 
            help.CAMINHO_MENU=form_help.menu_dir.data              
            help.CODIGO_MENU=form_help.menu_cod.data 
            help.PROBLEMA=form_help.problema.data
            help.ANALISADO=form_help.analisado.data
            help.DUVIDA=form_help.duvida.data
            help.PALIATIVA=form_help.paliativa.data
            help.BANCO=form_help.db_teste.data
            help.VERSAO=form_help.versao.data
            help.SOLUCAO=form_help.solucao.data
            help.DTA_CONCLUDED = datetime.utcnow()
            help.STATUS='CANCELADO'

            mov = MOV_SOL(NRO_TP=form_help.nro_tp.data, TITULO='Cancelamento de Help', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação cancelada', STATUS='CANCELADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailHelp(help.NRO_TP, 'H')

            flash('Solicitação Recusada', 'alert-success')

            return True 
    if form_help.validate_on_submit() and 'btn_submit_encaminhar' in request.form:
        help = HELP.query.filter_by(
            NRO_TP=form_help.nro_tp.data).first()
        
        if help:
            helper = HELPER.query.filter_by(USUARIO=form_help.helper.data).first()

            help.HELPER_ID=helper.id
            help.STATUS='NÃO INICIADO'

            mov = MOV_SOL(NRO_TP=form_help.nro_tp.data, TITULO='Solicitação Encaminhada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação teve seu helper trocado', STATUS='NÃO INICIADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailHelp(help.NRO_TP, 'I')

            flash('Solicitação Encaminhada', 'alert-success')

            return True  

def solHelpTime():
    result = HELP.query.filter_by(HELPER_ID=current_user.id)

    return result

def solHelpTimeGestor():
    result = HELP.query.filter().join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id)))

    return result

def solHelpTimeCoordenador():
    result = HELP.query.filter().all()

    return result

def enviaEmailHelp(tp_id, tipo):
    if tipo == 'H':
        helpID = HELP.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Solicitação de Informação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [helpID.requester.EMAIL],
                body = f'''
                Bom dia {helpID.requester.USUARIO},

                A solicitação de Help sobre a TP {helpID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'A':
        helpID = HELP.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Notificação de Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [helpID.finisher.EMAIL],
                body = f'''
                Bom dia {helpID.finisher.USUARIO},

                A solicitação de Help sobre a TP {helpID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'I':
        helpID = HELP.query.filter_by(NRO_TP=tp_id).first()
        helper = HELPER.query.filter_by(id=helpID.HELPER_ID).first()

        msg = Message(
                subject = 'Nova Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [helper.EMAIL],
                body = f'''
                Bom dia {helper.USUARIO},

                Foi criada uma solicitação de Help sobre a TP {helpID.NRO_TP},

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    else:
        flash('help', 'danger-success')

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
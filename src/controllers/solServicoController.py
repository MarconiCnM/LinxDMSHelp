import os
from datetime import datetime, timedelta
from flask import request, flash
from flask_login import current_user
from flask_mail import Message

from models.models import SOL_SERVICO, MOV_SOL, TIME, HELPER, ANALISTA
from app import app, database, mail, mail_settings


def solServico(form_servico):
    if form_servico.validate_on_submit() and 'btn_submit_inserir' in request.form:
        servico = SOL_SERVICO.query.filter_by(
            NRO_TP=form_servico.nro_tp.data).first()

        if servico:
            flash(
                'Já existe solicitação de analise de serviço para essa TP', 'alert-danger')
        else:
            time = TIME.query.filter_by(id=current_user.TIME_ID).first()
            helper = HELPER.query.filter_by(id=time.HELPER_ID).first()

            servico = SOL_SERVICO(NRO_TP=form_servico.nro_tp.data, FRANQUEADO=form_servico.franqueado.data, 
                            DESC=form_servico.descricao.data, ANALISE=form_servico.analise.data, 
                            SOLUCAO=form_servico.solucao.data, ANALISTA_ID=current_user.id, HELPER_ID=helper.id)

            database.session.add(servico)

            mov = MOV_SOL(NRO_TP=form_servico.nro_tp.data, TITULO='Abertura de Analise', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO='Solicitação de serviço aberta', STATUS='AGUARDANDO INICIALIZAÇÂO')
            database.session.add(mov)
            database.session.commit()

            enviaEmailServico(servico.NRO_TP, 'I')

            flash('Solicitação feita com sucesso', 'alert-success')

            return True

    if form_servico.validate_on_submit() and 'btn_submit_iniciar' in request.form:
        servico = SOL_SERVICO.query.filter_by(
            NRO_TP=form_servico.nro_tp.data).first()

        servico.NRO_TP=form_servico.nro_tp.data 
        servico.FRANQUEADO=form_servico.franqueado.data
        servico.DESC=form_servico.descricao.data
        servico.ANALISE=form_servico.analise.data
        servico.SOLUCAO=form_servico.solucao.data
        servico.HELPER_ID=current_user.id
        servico.STATUS = 'EM ANALISE'

        mov = MOV_SOL(NRO_TP=form_servico.nro_tp.data, TITULO='Analise Iniciada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Mov', STATUS='EM ANALISE')
        database.session.add(mov)
        database.session.commit()

        enviaEmailServico(servico.NRO_TP, 'H')

        flash('Analise Iniciada', 'alert-success')
        return True
        
    if form_servico.validate_on_submit() and 'btn_submit_info' in request.form:
        servico = SOL_SERVICO.query.filter_by(
            NRO_TP=form_servico.nro_tp.data).first()

        
        if form_servico.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua duvida ou requisição', 'alert-danger')
        else:
            servico.NRO_TP=form_servico.nro_tp.data 
            servico.FRANQUEADO=form_servico.franqueado.data
            servico.DESC=form_servico.descricao.data
            servico.ANALISE=form_servico.analise.data
            servico.SOLUCAO=form_servico.solucao.data
            servico.STATUS = 'AGUARDANDO INFORMAÇÃO'

            mov = MOV_SOL(NRO_TP=form_servico.nro_tp.data, TITULO='Solicitação de Informação', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO=form_servico.solucao.data, STATUS='AGUARDANDO INFORMAÇÃO')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailServico(servico.NRO_TP, 'H')

            flash('Aguardando Informação', 'alert-success')
            
            return True

    if form_servico.validate_on_submit() and 'btn_submit_infores' in request.form:
        servico = SOL_SERVICO.query.filter_by(
            NRO_TP=form_servico.nro_tp.data).first()

        
        if form_servico.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua resposta', 'alert-danger')
        else:
            servico.NRO_TP=form_servico.nro_tp.data 
            servico.FRANQUEADO=form_servico.franqueado.data
            servico.DESC=form_servico.descricao.data
            servico.ANALISE=form_servico.analise.data
            servico.SOLUCAO=form_servico.solucao.data
            servico.STATUS = 'EM ANALISE'

            mov = MOV_SOL(NRO_TP=form_servico.nro_tp.data, TITULO='Conclusão de Informação', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO=form_servico.solucao.data, STATUS='EM ANALISE')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailServico(servico.NRO_TP, 'A')
            
            flash('Enviada a Analise', 'alert-success')

            return True
    
    if form_servico.validate_on_submit() and 'btn_submit_final' in request.form:
        servico = SOL_SERVICO.query.filter_by(
            NRO_TP=form_servico.nro_tp.data).first()
        
        if form_servico.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            servico.NRO_TP=form_servico.nro_tp.data 
            servico.FRANQUEADO=form_servico.franqueado.data
            servico.DESC=form_servico.descricao.data
            servico.ANALISE=form_servico.analise.data
            servico.SOLUCAO=form_servico.solucao.data
            servico.DTA_CONCLUDED = datetime.utcnow()
            servico.STATUS='FINALIZADA'

            mov = MOV_SOL(NRO_TP=form_servico.nro_tp.data, TITULO='Solicitação Finalizada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação aprovada, não esqueça de ajustar a taxonomia do chamado para "service request"', STATUS='FINALIZADA')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailServico(servico.NRO_TP, 'H')

            flash('Solicitação Finalizada', 'alert-success')

            return True

    if form_servico.validate_on_submit() and 'btn_submit_recus' in request.form:
        servico = SOL_SERVICO.query.filter_by(
            NRO_TP=form_servico.nro_tp.data).first()
        
        if form_servico.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            servico.NRO_TP=form_servico.nro_tp.data 
            servico.FRANQUEADO=form_servico.franqueado.data
            servico.DESC=form_servico.descricao.data
            servico.ANALISE=form_servico.analise.data
            servico.SOLUCAO=form_servico.solucao.data
            servico.DTA_CONCLUDED = datetime.utcnow()
            servico.STATUS='NÃO APROVADO'

            mov = MOV_SOL(NRO_TP=form_servico.nro_tp.data, TITULO='Solicitação Recusada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação não aprovada', STATUS='NÃO APROVADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailServico(servico.NRO_TP, 'H')

            flash('Solicitação Recusada', 'alert-success')

            return True 

    if form_servico.validate_on_submit() and 'btn_submit_encaminhar' in request.form:
        servico = SOL_SERVICO.query.filter_by(
            NRO_TP=form_servico.nro_tp.data).first()
        
        if servico:
            helper = HELPER.query.filter_by(USUARIO=form_servico.helper.data).first()

            servico.HELPER_ID=helper.id
            servico.STATUS='NÃO INICIADO'

            mov = MOV_SOL(NRO_TP=form_servico.nro_tp.data, TITULO='Solicitação Encaminhada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação teve seu helper trocado', STATUS='NÃO INICIADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailServico(servico.NRO_TP, 'I')

            flash('Solicitação Encaminhada', 'alert-success')

            return True  

def solServicoTime():
    result = SOL_SERVICO.query.filter_by(HELPER_ID=current_user.id)

    return result

def solServicoTimeGestor():
    result = SOL_SERVICO.query.filter().join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id)))

    return result

def solServicoTimeCoordenador():
    result = SOL_SERVICO.query.filter()

    return result


def enviaEmailServico(tp_id, tipo):
    if tipo == 'H':
        servicoID = SOL_SERVICO.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Solicitação de Informação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [servicoID.requester.EMAIL],
                body = f'''
                Bom dia {servicoID.requester.USUARIO},

                A solicitação de analise de serviço sobre a TP {servicoID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'A':
        servicoID = SOL_SERVICO.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Notificação de Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [servicoID.finisher.EMAIL],
                body = f'''
                Bom dia {servicoID.finisher.USUARIO},

                A solicitação de analise de serviço sobre a TP {servicoID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'I':
        servicoID = SOL_SERVICO.query.filter_by(NRO_TP=tp_id).first()
        helper = HELPER.query.filter_by(id=servicoID.HELPER_ID).first()

        msg = Message(
                subject = 'Nova Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [helper.EMAIL],
                body = f'''
                Bom dia {helper.USUARIO},

                Foi criada uma solicitação de analise de serviço sobre a TP {servicoID.NRO_TP},

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
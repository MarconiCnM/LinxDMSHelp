import os
from datetime import datetime, timedelta
from flask import request, flash
from flask_login import current_user
from flask_mail import Message

from models.models import SOL_SHARE, MOV_SOL, TIME, HELPER, ANALISTA
from app import app, database, mail, mail_settings


def solShare(form_share):
    if form_share.validate_on_submit() and 'btn_submit_inserir' in request.form:
        time = TIME.query.filter_by(id=current_user.TIME_ID).first()
        helper = HELPER.query.filter_by(id=time.HELPER_ID).first()


        if SOL_SHARE.query.filter_by(TITULO=form_share.titulo.data).first():
            flash('Já existe um share com esse mesmo Titulo favor validar se já não existe share sobre isso.', 'alert-danger')
        else:
            share = SOL_SHARE(TITULO=form_share.titulo.data, PRODUTO=form_share.produto.data, MODULO=form_share.modulo.data, 
                            FINALIDADE=form_share.finalidade.data, LINK=form_share.link.data,
                            SOLUCAO=form_share.solucao.data, ANALISTA_ID=current_user.id, HELPER_ID=helper.id)

            database.session.add(share)
            database.session.commit()

            share = SOL_SHARE.query.filter_by(TITULO=form_share.titulo.data).first()

            mov = MOV_SOL(NRO_TP=share.id, TITULO='Abertura de Analise', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO='Solicitação de serviço aberta', STATUS='AGUARDANDO INICIALIZAÇÂO')
            database.session.add(mov)
            database.session.commit()

            enviaEmailShare(share.id, 'I')

            flash('Solicitação feita com sucesso', 'alert-success')

            return True

    if form_share.validate_on_submit() and 'btn_submit_iniciar' in request.form:
        share = SOL_SHARE.query.filter_by(TITULO=form_share.titulo.data).first()

        share.TITULO=form_share.titulo.data 
        share.PRODUTO=form_share.produto.data
        share.MODULO=form_share.modulo.data
        share.FINALIDADE=form_share.finalidade.data
        share.LINK=form_share.link.data
        share.SOLUCAO=form_share.solucao.data
        share.HELPER_ID=current_user.id
        share.STATUS = 'EM ANALISE'

        database.session.add(share)

        mov = MOV_SOL(NRO_TP=share.id, TITULO='Analise Iniciada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Mov', STATUS='EM ANALISE')
        database.session.add(mov)
        database.session.commit()

        enviaEmailShare(share.id, 'H')

        flash('Analise Iniciada', 'alert-success')
        return True

    if form_share.validate_on_submit() and 'btn_submit_info' in request.form:
        share = SOL_SHARE.query.filter_by(TITULO=form_share.titulo.data).first()

        
        if form_share.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua duvida ou requisição', 'alert-danger')
        else:
            share.TITULO=form_share.titulo.data 
            share.PRODUTO=form_share.produto.data
            share.MODULO=form_share.modulo.data
            share.FINALIDADE=form_share.finalidade.data
            share.LINK=form_share.link.data
            share.SOLUCAO=form_share.solucao.data
            share.STATUS = 'AGUARDANDO INFORMAÇÃO'

            mov = MOV_SOL(NRO_TP=share.id, TITULO='Solicitação de Informação', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO=form_share.solucao.data, STATUS='AGUARDANDO INFORMAÇÃO')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailShare(share.id, 'H')

            flash('Aguardando Informação', 'alert-success')
            
            return True

    if form_share.validate_on_submit() and 'btn_submit_infores' in request.form:
        share = SOL_SHARE.query.filter_by(TITULO=form_share.titulo.data).first()

        
        if form_share.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua resposta', 'alert-danger')
        else:
            share.TITULO=form_share.titulo.data 
            share.PRODUTO=form_share.produto.data
            share.MODULO=form_share.modulo.data
            share.FINALIDADE=form_share.finalidade.data
            share.LINK=form_share.link.data
            share.SOLUCAO=form_share.solucao.data
            share.STATUS = 'EM ANALISE'

            mov = MOV_SOL(NRO_TP=share.id, TITULO='Conclusão de Informação', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO=form_share.solucao.data, STATUS='EM ANALISE')
            
            database.session.add(mov)
            database.session.commit()   
            
            enviaEmailShare(share.id, 'A')
            
            flash('Enviada a Analise', 'alert-success')

            return True

    if form_share.validate_on_submit() and 'btn_submit_recus' in request.form:
        share = SOL_SHARE.query.filter_by(TITULO=form_share.titulo.data).first()


        if form_share.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            share.TITULO=form_share.titulo.data 
            share.PRODUTO=form_share.produto.data
            share.MODULO=form_share.modulo.data
            share.FINALIDADE=form_share.finalidade.data
            share.LINK=form_share.link.data
            share.SOLUCAO=form_share.solucao.data
            share.DTA_CONCLUDED = datetime.utcnow()
            share.STATUS='NÃO APROVADO'

            mov = MOV_SOL(NRO_TP=share.id, TITULO='Solicitação Recusada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação não aprovada', STATUS='NÃO APROVADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailShare(share.id, 'H')

            flash('Solicitação Recusada', 'alert-success')

            return True 

    if form_share.validate_on_submit() and 'btn_submit_final' in request.form:
        share = SOL_SHARE.query.filter_by(TITULO=form_share.titulo.data).first()
        
        if form_share.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            share.TITULO=form_share.titulo.data 
            share.PRODUTO=form_share.produto.data
            share.MODULO=form_share.modulo.data
            share.FINALIDADE=form_share.finalidade.data
            share.LINK=form_share.link.data
            share.SOLUCAO=form_share.solucao.data
            share.DTA_CONCLUDED = datetime.utcnow()
            share.STATUS='FINALIZADA'

            mov = MOV_SOL(NRO_TP=share.id, TITULO='Solicitação Finalizada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Share Aprovado', STATUS='FINALIZADA')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailShare(share.id, 'H')

            flash('Solicitação Finalizada', 'alert-success')

            return True
    
    if form_share.validate_on_submit() and 'btn_submit_encaminhar' in request.form:
        share = SOL_SHARE.query.filter_by(TITULO=form_share.titulo.data).first()
        
        if share:
            helper = HELPER.query.filter_by(USUARIO=form_share.helper.data).first()

            share.HELPER_ID=helper.id
            share.STATUS='NÃO INICIADO'

            mov = MOV_SOL(NRO_TP=share.id, TITULO='Solicitação Encaminhada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação teve seu helper trocado', STATUS='NÃO INICIADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailShare(share.id, 'I')

            flash('Solicitação Encaminhada', 'alert-success')

            return True    


def solShareTime():
    result = SOL_SHARE.query.filter_by(HELPER_ID=current_user.id)

    return result

def solShareTimeGestor():
    result = SOL_SHARE.query.filter().join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id)))

    return result

def solShareTimeCoordenador():
    result = SOL_SHARE.query.filter().all()
    
    return result



def enviaEmailShare(tp_id, tipo):
    if tipo == 'H':
        shareID = SOL_SHARE.query.filter_by(id=tp_id).first()
        msg = Message(
                subject = 'Solicitação de Informação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [shareID.requester.EMAIL],
                body = f'''
                Bom dia {shareID.requester.USUARIO},

                A solicitação de analise de share,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'A':
        shareID = SOL_SHARE.query.filter_by(id=tp_id).first()
        msg = Message(
                subject = 'Notificação de Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [shareID.finisher.EMAIL],
                body = f'''
                Bom dia {shareID.finisher.USUARIO},

                A solicitação de analise de share,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'I':
        shareID = SOL_SHARE.query.filter_by(id=tp_id).first()
        helper = HELPER.query.filter_by(id=shareID.HELPER_ID).first()

        msg = Message(
                subject = 'Nova Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [helper.EMAIL],
                body = f'''
                Bom dia {helper.USUARIO},

                Foi criada uma solicitação de analise de share,

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
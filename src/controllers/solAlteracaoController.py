import os
from datetime import datetime, timedelta
from flask import request, flash
from flask_login import current_user
from flask_mail import Message

from models.models import SOL_HISTORIA, MOV_SOL, TIME, HELPER, ANALISTA
from app import app, database, mail, mail_settings
from datetime import datetime

def solAlteracao(form_alteracao):
    if form_alteracao.validate_on_submit() and 'btn_submit_inserir' in request.form:
        alteracao = SOL_HISTORIA.query.filter_by(
            NRO_TP=form_alteracao.nro_tp.data).first()

        if alteracao:
            flash(
                'Já existe solicitação de analise de alteração para essa TP', 'alert-danger')
        elif form_alteracao.docs.data is None:
            flash(
                'Por favor adicione os arquivos', 'alert-danger')
        else:
            time = TIME.query.filter_by(id=current_user.TIME_ID).first()
            helper = HELPER.query.filter_by(id=time.HELPER_ID).first()

            name, extension = os.path.splitext(
                form_alteracao.docs.data.filename)
            name = str(form_alteracao.nro_tp.data) + '-' + \
                datetime.today().strftime('%d-%m-%Y.%H:%M')
            complete_name = name + extension
            complete_path = os.path.join(
                app.root_path, 'static', 'docs', 'alteracao', complete_name)

            form_alteracao.docs.data.save(complete_path)

            alteracao = SOL_HISTORIA(NRO_TP=form_alteracao.nro_tp.data, ISSUE='N', FAZENDO=form_alteracao.fazendo.data, 
                                FAZER=form_alteracao.fazer.data, COMO=form_alteracao.como.data, 
                                BENEFICIO=form_alteracao.beneficio.data, DOCS=complete_name,  ALT_CUST=form_alteracao.alt_cust.data,
                                VERSAO=form_alteracao.versao.data, ANALISTA_ID=current_user.id, HELPER_ID=helper.id)
            database.session.add(alteracao)

            mov = MOV_SOL(NRO_TP=form_alteracao.nro_tp.data, TITULO='Abertura de Analise', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO='Solicitação de historia aberta', STATUS='AGUARDANDO INICIALIZAÇÂO')
            database.session.add(mov)
            database.session.commit()

            enviaEmailAlteracao(alteracao.NRO_TP, 'I')

            flash('Solicitação feita com sucesso', 'alert-success')

            return True

    if form_alteracao.validate_on_submit() and 'btn_submit_iniciar' in request.form:
        alteracao = SOL_HISTORIA.query.filter_by(
            NRO_TP=form_alteracao.nro_tp.data).first()

        alteracao.NRO_TP=form_alteracao.nro_tp.data 
        alteracao.ISSUE=form_alteracao.issue.data
        alteracao.FAZENDO=form_alteracao.fazendo.data
        alteracao.FAZER=form_alteracao.fazer.data
        alteracao.COMO=form_alteracao.como.data
        alteracao.BENEFICIO=form_alteracao.beneficio.data
        alteracao.VERSAO=form_alteracao.versao.data
        alteracao.ALT_CUST=form_alteracao.alt_cust.data
        alteracao.SOLUCAO=form_alteracao.solucao.data
        alteracao.HELPER_ID=current_user.id
        alteracao.STATUS = 'EM ANALISE'

        mov = MOV_SOL(NRO_TP=form_alteracao.nro_tp.data, TITULO='Analise Iniciada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Mov', STATUS='EM ANALISE')
        database.session.add(mov)
        database.session.commit()

        enviaEmailAlteracao(alteracao.NRO_TP, 'H')

        flash('Analise Iniciada', 'alert-success')
        return True

    if form_alteracao.validate_on_submit() and 'btn_submit_aprov' in request.form:
        alteracao = SOL_HISTORIA.query.filter_by(
            NRO_TP=form_alteracao.nro_tp.data).first()

        alteracao.NRO_TP=form_alteracao.nro_tp.data 
        alteracao.ISSUE=form_alteracao.issue.data
        alteracao.FAZENDO=form_alteracao.fazendo.data
        alteracao.FAZER=form_alteracao.fazer.data
        alteracao.COMO=form_alteracao.como.data
        alteracao.BENEFICIO=form_alteracao.beneficio.data
        alteracao.VERSAO=form_alteracao.versao.data
        alteracao.ALT_CUST=form_alteracao.alt_cust.data
        alteracao.SOLUCAO=form_alteracao.solucao.data
        alteracao.STATUS = 'AGUARDANDO ABERTURA DE ISSUE'

        mov = MOV_SOL(NRO_TP=form_alteracao.nro_tp.data, TITULO='Aprovação de Abertura de ISSUE', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação aprovada, apos a abertura da issue não esqueça de vincular o numero na solicitação para adição do rotulo de aprovação', STATUS='AGUARDANDO ABERTURA DE ISSUE')
        
        database.session.add(mov)
        database.session.commit()
        
        enviaEmailAlteracao(alteracao.NRO_TP, 'H')
        
        flash('Aprovada Abertura de ISSUE', 'alert-success')
        
        return True

    if form_alteracao.validate_on_submit() and 'btn_submit_info' in request.form:
        alteracao = SOL_HISTORIA.query.filter_by(
            NRO_TP=form_alteracao.nro_tp.data).first()

        
        if form_alteracao.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua duvida ou requisição', 'alert-danger')
        else:
            alteracao.NRO_TP=form_alteracao.nro_tp.data 
            alteracao.ISSUE=form_alteracao.issue.data
            alteracao.FAZENDO=form_alteracao.fazendo.data
            alteracao.FAZER=form_alteracao.fazer.data
            alteracao.COMO=form_alteracao.como.data
            alteracao.BENEFICIO=form_alteracao.beneficio.data
            alteracao.VERSAO=form_alteracao.versao.data
            alteracao.ALT_CUST=form_alteracao.alt_cust.data
            alteracao.STATUS = 'AGUARDANDO INFORMAÇÃO'

            mov = MOV_SOL(NRO_TP=form_alteracao.nro_tp.data, TITULO='Solicitação de Informação', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO=form_alteracao.solucao.data, STATUS='AGUARDANDO INFORMAÇÃO')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailAlteracao(alteracao.NRO_TP, 'H')

            flash('Aguardando Informação', 'alert-success')
            
            return True

    if form_alteracao.validate_on_submit() and 'btn_submit_infores' in request.form:
        alteracao = SOL_HISTORIA.query.filter_by(
            NRO_TP=form_alteracao.nro_tp.data).first()

        
        if form_alteracao.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua resposta', 'alert-danger')
        else:
            alteracao.NRO_TP=form_alteracao.nro_tp.data 
            alteracao.ISSUE=form_alteracao.issue.data
            alteracao.FAZENDO=form_alteracao.fazendo.data
            alteracao.FAZER=form_alteracao.fazer.data
            alteracao.COMO=form_alteracao.como.data
            alteracao.BENEFICIO=form_alteracao.beneficio.data
            alteracao.VERSAO=form_alteracao.versao.data
            alteracao.ALT_CUST=form_alteracao.alt_cust.data
            alteracao.STATUS = 'EM ANALISE'

            mov = MOV_SOL(NRO_TP=form_alteracao.nro_tp.data, TITULO='Conclusão de Informação', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO=form_alteracao.solucao.data, STATUS='EM ANALISE')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailAlteracao(alteracao.NRO_TP, 'A')
            
            flash('Enviada a Analise', 'alert-success')

            return True
    
    if form_alteracao.validate_on_submit() and 'btn_submit_rotulo' in request.form:
        alteracao = SOL_HISTORIA.query.filter_by(
            NRO_TP=form_alteracao.nro_tp.data).first()

        if not form_alteracao.issue.data.find('AUTO-'):
            flash(
                'Por favor informe a issue aberta', 'alert-danger')
        else:
            alteracao.NRO_TP=form_alteracao.nro_tp.data 
            alteracao.ISSUE=form_alteracao.issue.data
            alteracao.FAZENDO=form_alteracao.fazendo.data
            alteracao.FAZER=form_alteracao.fazer.data
            alteracao.COMO=form_alteracao.como.data
            alteracao.BENEFICIO=form_alteracao.beneficio.data
            alteracao.VERSAO=form_alteracao.versao.data
            alteracao.ALT_CUST=form_alteracao.alt_cust.data
            alteracao.SOLUCAO=form_alteracao.solucao.data
            alteracao.STATUS='AGUARDANDO ADIÇÃO DE ROTULO'

            mov = MOV_SOL(NRO_TP=form_alteracao.nro_tp.data, TITULO='Solicitação de rotulo no JIRA', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO='ISSUE aberta e informada na solicitação favor adicionar o rotulo', STATUS='AGUARDANDO ADIÇÃO DE ROTULO')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailAlteracao(alteracao.NRO_TP, 'A')

            flash('Solicitação de rotulo no JIRA', 'alert-success')
            
            return True
        
    if form_alteracao.validate_on_submit() and 'btn_submit_final' in request.form:
        alteracao = SOL_HISTORIA.query.filter_by(
            NRO_TP=form_alteracao.nro_tp.data).first()
        
        if form_alteracao.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            alteracao.NRO_TP=form_alteracao.nro_tp.data 
            alteracao.ISSUE=form_alteracao.issue.data
            alteracao.FAZENDO=form_alteracao.fazendo.data
            alteracao.FAZER=form_alteracao.fazer.data
            alteracao.COMO=form_alteracao.como.data
            alteracao.BENEFICIO=form_alteracao.beneficio.data
            alteracao.VERSAO=form_alteracao.versao.data
            alteracao.ALT_CUST=form_alteracao.alt_cust.data
            alteracao.SOLUCAO=form_alteracao.solucao.data
            alteracao.DTA_CONCLUDED = datetime.utcnow()
            alteracao.STATUS='FINALIZADA'

            mov = MOV_SOL(NRO_TP=form_alteracao.nro_tp.data, TITULO='Solicitação Finalizada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Rotulo adicionado e solicitação finalizada', STATUS='FINALIZADA')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailAlteracao(alteracao.NRO_TP, 'H')
            enviaEmailAlteracao(alteracao.NRO_TP, 'F')

            flash('Solicitação Finalizada', 'alert-success')

            return True
    if form_alteracao.validate_on_submit() and 'btn_submit_recus' in request.form:
        alteracao = SOL_HISTORIA.query.filter_by(
            NRO_TP=form_alteracao.nro_tp.data).first()
        
        if form_alteracao.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            alteracao.NRO_TP=form_alteracao.nro_tp.data 
            alteracao.ISSUE=form_alteracao.issue.data
            alteracao.FAZENDO=form_alteracao.fazendo.data
            alteracao.FAZER=form_alteracao.fazer.data
            alteracao.COMO=form_alteracao.como.data
            alteracao.BENEFICIO=form_alteracao.beneficio.data
            alteracao.VERSAO=form_alteracao.versao.data
            alteracao.ALT_CUST=form_alteracao.alt_cust.data
            alteracao.SOLUCAO=form_alteracao.solucao.data
            alteracao.DTA_CONCLUDED = datetime.utcnow()
            alteracao.STATUS='NÃO APROVADO'

            mov = MOV_SOL(NRO_TP=form_alteracao.nro_tp.data, TITULO='Solicitação Recusada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação não aprovada', STATUS='NÃO APROVADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailAlteracao(alteracao.NRO_TP, 'H')

            flash('Solicitação Recusada', 'alert-success')

            return True 
    if form_alteracao.validate_on_submit() and 'btn_submit_encaminhar' in request.form:
        alteracao = SOL_HISTORIA.query.filter_by(
            NRO_TP=form_alteracao.nro_tp.data).first()
        
        if alteracao:
            helper = HELPER.query.filter_by(USUARIO=form_alteracao.helper.data).first()

            alteracao.HELPER_ID=helper.id
            alteracao.STATUS='NÃO INICIADO'

            mov = MOV_SOL(NRO_TP=form_alteracao.nro_tp.data, TITULO='Solicitação Encaminhada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação teve seu helper trocado', STATUS='NÃO INICIADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailAlteracao(alteracao.NRO_TP, 'I')

            flash('Solicitação Encaminhada', 'alert-success')

            return True 

def solAlteracaoTime():
    result = SOL_HISTORIA.query.filter_by(HELPER_ID=current_user.id)

    return result

def solAlteracaoTimeGestor():
    result = SOL_HISTORIA.query.filter().join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id)))

    return result

def solAlteracaoTimeCoordenador():
    result = SOL_HISTORIA.query.filter().all()

    return result

def enviaEmailAlteracao(tp_id, tipo):
    if tipo == 'H':
        erroID = SOL_HISTORIA.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Solicitação de Informação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [erroID.requester.EMAIL],
                body = f'''
                Bom dia {erroID.requester.USUARIO},

                A solicitação de analise de historia sobre a TP {erroID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'A':
        erroID = SOL_HISTORIA.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Notificação de Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [erroID.finisher.EMAIL],
                body = f'''
                Bom dia {erroID.finisher.USUARIO},

                A solicitação de analise de historia sobre a TP {erroID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'I':
        erroID = SOL_HISTORIA.query.filter_by(NRO_TP=tp_id).first()
        helper = HELPER.query.filter_by(id=erroID.HELPER_ID).first()

        msg = Message(
                subject = 'Nova Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [helper.EMAIL],
                body = f'''
                Bom dia {helper.USUARIO},

                Foi criada uma solicitação de analise de historia sobre a TP {erroID.NRO_TP},

                Atenciosamente,
                Suporte Help
                '''
            )

        #mail.send(msg)
    elif tipo == 'F':
        altID = SOL_HISTORIA.query.filter_by(NRO_TP=tp_id).first()
        helper = HELPER.query.filter_by(id=altID.HELPER_ID).first()

        msg = Message(
                subject = f'ISSUE Aberta - {altID.ISSUE}',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= ['apollo@linx.com.br','bravos@linx.com.br'],
                body = f'''Bom dia Pessoal,

Segue ISSUE encaminhada para {altID.ALT_CUST},

*Solicitante:* {altID.requester.USUARIO}
*Aprovador:* {altID.finisher.USUARIO}

*O que o sistema está fazendo:* {altID.FAZENDO}

*O que o sistema deveria fazer:* {altID.FAZER}

*Como deseja que o sistema faça:* {altID.COMO}

*Qual o beneficio dessa alteração:* {altID.BENEFICIO}

*Versão:* {altID.VERSAO}

Atenciosamente,
Suporte Help
                ''')

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
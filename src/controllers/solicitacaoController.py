import os
from datetime import datetime, timedelta
from flask import request, flash
from flask_login import current_user
from flask_mail import Message

from models.models import SOL_ERRO, MOV_SOL, ANALISTA, TIME, HELPER
from app import app, database, mail, mail_settings
from datetime import datetime


def solErro(form_erro):
    if form_erro.validate_on_submit() and 'btn_submit_inserir' in request.form:
        erro = SOL_ERRO.query.filter_by(
            NRO_TP=form_erro.nro_tp.data).first()

        if erro:
            flash(
                'Já existe solicitação de analise de erro para essa TP', 'alert-danger')
        elif form_erro.docs.data is None:
            flash(
                'Por favor adicione os arquivos', 'alert-danger')
        else:
            name, extension = os.path.splitext(
                form_erro.docs.data.filename)
            name = str(form_erro.nro_tp.data) + '-' + \
                datetime.today().strftime('%d-%m-%Y.%H:%M')
            complete_name = name + extension
            complete_path = os.path.join(
                app.root_path, 'static', 'docs', 'erro', complete_name)
            form_erro.docs.data.save(complete_path)

            erro = SOL_ERRO(NRO_TP=form_erro.nro_tp.data, ISSUE='N', CAMINHO_MENU=form_erro.menu_dir.data, 
                            CODIGO_MENU=form_erro.menu_cod.data, FAZENDO=form_erro.fazer.data, FAZER=form_erro.fazer.data, 
                            PALIATIVA=form_erro.paliativa.data, DOCS=complete_name, BANCO=form_erro.db_teste.data, VERSAO=form_erro.versao.data, 
                            VERSAO_ANT=form_erro.versao_ant.data, ANALISTA_ID=current_user.id)
            database.session.add(erro)

            mov = MOV_SOL(NRO_TP=form_erro.nro_tp.data, TITULO='Abertura de Analise', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO='Solicitação de erro aberta', STATUS='AGUARDANDO INICIALIZAÇÂO')
            database.session.add(mov)
            database.session.commit()

            enviaEmailErro(erro.NRO_TP, 'I')

            flash('Solicitação feita com sucesso', 'alert-success')

            return True

    if form_erro.validate_on_submit() and 'btn_submit_iniciar' in request.form:
        erro = SOL_ERRO.query.filter_by(
            NRO_TP=form_erro.nro_tp.data).first()

        erro.NRO_TP=form_erro.nro_tp.data 
        erro.ISSUE=form_erro.issue.data
        erro.CAMINHO_MENU=form_erro.menu_dir.data              
        erro.CODIGO_MENU=form_erro.menu_cod.data 
        erro.FAZENDO=form_erro.fazer.data
        erro.FAZER=form_erro.fazer.data
        erro.PALIATIVA=form_erro.paliativa.data
        erro.BANCO=form_erro.db_teste.data
        erro.VERSAO=form_erro.versao.data
        erro.VERSAO_ANT=form_erro.versao_ant.data
        erro.SOLUCAO=form_erro.solucao.data
        erro.HELPER_ID=current_user.id
        erro.STATUS = 'EM ANALISE'

        mov = MOV_SOL(NRO_TP=form_erro.nro_tp.data, TITULO='Analise Iniciada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Mov', STATUS='EM ANALISE')
        database.session.add(mov)
        database.session.commit()

        enviaEmailErro(erro.NRO_TP, 'H')

        flash('Analise Iniciada', 'alert-success')
        return True

    if form_erro.validate_on_submit() and 'btn_submit_aprov' in request.form:
        erro = SOL_ERRO.query.filter_by(
            NRO_TP=form_erro.nro_tp.data).first()

        erro.NRO_TP=form_erro.nro_tp.data 
        erro.ISSUE=form_erro.issue.data
        erro.CAMINHO_MENU=form_erro.menu_dir.data              
        erro.CODIGO_MENU=form_erro.menu_cod.data 
        erro.FAZENDO=form_erro.fazer.data
        erro.FAZER=form_erro.fazer.data
        erro.PALIATIVA=form_erro.paliativa.data
        erro.BANCO=form_erro.db_teste.data
        erro.VERSAO=form_erro.versao.data
        erro.VERSAO_ANT=form_erro.versao_ant.data
        erro.SOLUCAO=form_erro.solucao.data
        erro.STATUS = 'AGUARDANDO ABERTURA DE ISSUE'

        mov = MOV_SOL(NRO_TP=form_erro.nro_tp.data, TITULO='Aprovação de Abertura de ISSUE', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação aprovada, apos a abertura da issue não esqueça de vincular o numero na solicitação para adição do rotulo de aprovação', STATUS='AGUARDANDO ABERTURA DE ISSUE')
        
        database.session.add(mov)
        database.session.commit()
        
        enviaEmailErro(erro.NRO_TP, 'H')
        
        flash('Aprovada Abertura de ISSUE', 'alert-success')
        
        return True

    if form_erro.validate_on_submit() and 'btn_submit_info' in request.form:
        erro = SOL_ERRO.query.filter_by(
            NRO_TP=form_erro.nro_tp.data).first()

        
        if form_erro.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua duvida ou requisição', 'alert-danger')
        else:
            erro.NRO_TP=form_erro.nro_tp.data 
            erro.ISSUE=form_erro.issue.data
            erro.CAMINHO_MENU=form_erro.menu_dir.data              
            erro.CODIGO_MENU=form_erro.menu_cod.data 
            erro.FAZENDO=form_erro.fazer.data
            erro.FAZER=form_erro.fazer.data
            erro.PALIATIVA=form_erro.paliativa.data
            erro.BANCO=form_erro.db_teste.data
            erro.VERSAO=form_erro.versao.data
            erro.VERSAO_ANT=form_erro.versao_ant.data
            erro.STATUS = 'AGUARDANDO INFORMAÇÃO'

            mov = MOV_SOL(NRO_TP=form_erro.nro_tp.data, TITULO='Solicitação de Informação', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO=form_erro.solucao.data, STATUS='AGUARDANDO INFORMAÇÃO')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailErro(erro.NRO_TP, 'H')

            flash('Aguardando Informação', 'alert-success')
            
            return True

    if form_erro.validate_on_submit() and 'btn_submit_infores' in request.form:
        erro = SOL_ERRO.query.filter_by(
            NRO_TP=form_erro.nro_tp.data).first()

        
        if form_erro.solucao.data == '':
            flash(
                'Por favor digite no campo solução sua resposta', 'alert-danger')
        else:
            erro.NRO_TP=form_erro.nro_tp.data 
            erro.ISSUE=form_erro.issue.data
            erro.CAMINHO_MENU=form_erro.menu_dir.data              
            erro.CODIGO_MENU=form_erro.menu_cod.data 
            erro.FAZENDO=form_erro.fazer.data
            erro.FAZER=form_erro.fazer.data
            erro.PALIATIVA=form_erro.paliativa.data
            erro.BANCO=form_erro.db_teste.data
            erro.VERSAO=form_erro.versao.data
            erro.VERSAO_ANT=form_erro.versao_ant.data
            erro.STATUS = 'EM ANALISE'

            mov = MOV_SOL(NRO_TP=form_erro.nro_tp.data, TITULO='Conclusão de Informação', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO=form_erro.solucao.data, STATUS='EM ANALISE')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailErro(erro.NRO_TP, 'A')
            
            flash('Enviada a Analise', 'alert-success')

            return True
            
    if form_erro.validate_on_submit() and 'btn_submit_rotulo' in request.form:
        erro = SOL_ERRO.query.filter_by(
            NRO_TP=form_erro.nro_tp.data).first()
        
        print(form_erro.issue.data)

        if form_erro.issue.data == '':
            flash(
                'Por favor informe a issue aberta', 'alert-danger')
        else:
            erro.NRO_TP=form_erro.nro_tp.data 
            erro.ISSUE=form_erro.issue.data
            erro.CAMINHO_MENU=form_erro.menu_dir.data              
            erro.CODIGO_MENU=form_erro.menu_cod.data 
            erro.FAZENDO=form_erro.fazer.data
            erro.FAZER=form_erro.fazer.data
            erro.PALIATIVA=form_erro.paliativa.data
            erro.BANCO=form_erro.db_teste.data
            erro.VERSAO=form_erro.versao.data
            erro.VERSAO_ANT=form_erro.versao_ant.data
            erro.SOLUCAO=form_erro.solucao.data
            erro.STATUS='AGUARDANDO ADIÇÃO DE ROTULO'

            mov = MOV_SOL(NRO_TP=form_erro.nro_tp.data, TITULO='Solicitação de rotulo no JIRA', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO='ISSUE aberta e informada na solicitação favor adicionar o rotulo', STATUS='AGUARDANDO ADIÇÃO DE ROTULO')
            
            database.session.add(mov)
            database.session.commit()
            
            enviaEmailErro(erro.NRO_TP, 'A')

            flash('Solicitação de rotulo no JIRA', 'alert-success')
            
            return True
        
    if form_erro.validate_on_submit() and 'btn_submit_final' in request.form:
        erro = SOL_ERRO.query.filter_by(
            NRO_TP=form_erro.nro_tp.data).first()
        
        if form_erro.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            erro.NRO_TP=form_erro.nro_tp.data 
            erro.ISSUE=form_erro.issue.data
            erro.CAMINHO_MENU=form_erro.menu_dir.data              
            erro.CODIGO_MENU=form_erro.menu_cod.data 
            erro.FAZENDO=form_erro.fazer.data
            erro.FAZER=form_erro.fazer.data
            erro.PALIATIVA=form_erro.paliativa.data
            erro.BANCO=form_erro.db_teste.data
            erro.VERSAO=form_erro.versao.data
            erro.VERSAO_ANT=form_erro.versao_ant.data
            erro.SOLUCAO=form_erro.solucao.data
            erro.DTA_CONCLUDED = datetime.utcnow()
            erro.STATUS='FINALIZADA'

            mov = MOV_SOL(NRO_TP=form_erro.nro_tp.data, TITULO='Solicitação Finalizada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Rotulo adicionado e solicitação finalizada', STATUS='FINALIZADA')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailErro(erro.NRO_TP, 'H')

            flash('Solicitação Finalizada', 'alert-success')

            return True
    if form_erro.validate_on_submit() and 'btn_submit_recus' in request.form:
        erro = SOL_ERRO.query.filter_by(
            NRO_TP=form_erro.nro_tp.data).first()
        
        if form_erro.solucao.data == '':
            flash(
                'Por favor informe a resolução', 'alert-danger')
        else:
            erro.NRO_TP=form_erro.nro_tp.data 
            erro.ISSUE=form_erro.issue.data
            erro.CAMINHO_MENU=form_erro.menu_dir.data              
            erro.CODIGO_MENU=form_erro.menu_cod.data 
            erro.FAZENDO=form_erro.fazer.data
            erro.FAZER=form_erro.fazer.data
            erro.PALIATIVA=form_erro.paliativa.data
            erro.BANCO=form_erro.db_teste.data
            erro.VERSAO=form_erro.versao.data
            erro.VERSAO_ANT=form_erro.versao_ant.data
            erro.SOLUCAO=form_erro.solucao.data
            erro.DTA_CONCLUDED = datetime.utcnow()
            erro.STATUS='NÃO APROVADO'

            mov = MOV_SOL(NRO_TP=form_erro.nro_tp.data, TITULO='Solicitação Recusada', TIPO='H', HELPER=current_user.USUARIO, ANALISTA='', RESUMO='Solicitação não aprovada', STATUS='NÃO APROVADO')
            
            database.session.add(mov)
            database.session.commit()

            enviaEmailErro(erro.NRO_TP, 'H')

            flash('Solicitação Recusada', 'alert-success')

            return True 

def solErroTime():
    result = SOL_ERRO.query.join(ANALISTA).join(TIME).filter_by(HELPER_ID=current_user.id)

    return result

def enviaEmailErro(tp_id, tipo):
    if tipo == 'H':
        erroID = SOL_ERRO.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Solicitação de Informação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [erroID.requester.EMAIL],
                body = f'''
                Bom dia {erroID.requester.USUARIO},

                A solicitação de analise de erro sobre a TP {erroID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        mail.send(msg)
    elif tipo == 'A':
        erroID = SOL_ERRO.query.filter_by(NRO_TP=tp_id).first()
        msg = Message(
                subject = 'Notificação de Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [erroID.finisher.EMAIL],
                body = f'''
                Bom dia {erroID.finisher.USUARIO},

                A solicitação de analise de erro sobre a TP {erroID.NRO_TP} teve uma interação,

                Atenciosamente,
                Suporte Help
                '''
            )

        mail.send(msg)
    elif tipo == 'I':
        erroID = SOL_ERRO.query.filter_by(NRO_TP=tp_id).first()
        time = TIME.query.filter_by(id=current_user.TIME_ID).first()
        helper = HELPER.query.filter_by(id=time.HELPER_ID).first()

        msg = Message(
                subject = 'Nova Soliticação - LinxDMS HELP',
                sender = mail_settings["MAIL_USERNAME"],
                recipients= [helper.EMAIL],
                body = f'''
                Bom dia {helper.USUARIO},

                Foi criada uma solicitação de analise de erro sobre a TP {erroID.NRO_TP},

                Atenciosamente,
                Suporte Help
                '''
            )

        mail.send(msg)
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
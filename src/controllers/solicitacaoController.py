import os
from datetime import datetime, timedelta
from flask import request, flash
from flask_login import current_user

from models.models import SOL_HISTORIA, SOL_ERRO, MOV_SOL
from app import app, database, bcrypt
import datetime

def solAlteracao(form_alteracao):
    if form_alteracao.validate_on_submit() and 'btn_submit_salvar' in request.form:
        alteracao = SOL_HISTORIA.query.filter_by(
            NRO_TP=form_alteracao.nro_tp.data).first()

        alteracao.NRO_TP = form_alteracao.nro_tp.data
        alteracao.ISSUE = form_alteracao.issue.data
        alteracao.FAZENDO = form_alteracao.fazendo.data
        alteracao.FAZER = form_alteracao.fazer.data
        alteracao.COMO = form_alteracao.como.data
        alteracao.VERSAO = form_alteracao.versao.data
        alteracao.DOCS = form_alteracao.docs.data
        alteracao.ALT_CUST = form_alteracao.alt_cust.data
        alteracao.SOLUCAO = form_alteracao.solucao.data
        alteracao.STATUS = ''
        database.session.commit()

    elif form_alteracao.validate_on_submit() and 'btn_submit_inserir' in request.form:
        alteracao = SOL_HISTORIA.query.filter_by(
            NRO_TP=form_alteracao.nro_tp.data).first()

        if alteracao:
            flash(
                'Já existe solicitação de alteração para essa TP', 'alert-danger')
        else:
            name, extension = os.path.splitext(
                form_alteracao.docs.data.filename)
            name = str(form_alteracao.nro_tp.data) + '-' + \
                datetime.today().strftime('%d-%m-%Y.%H:%M')
            complete_name = name + extension
            complete_path = os.path.join(
                app.root_path, 'static', 'docs', 'alteracao', complete_name)
            form_alteracao.docs.data.save(complete_path)

            alteracao = SOL_HISTORIA(NRO_TP=form_alteracao.nro_tp.data, ISSUE=form_alteracao.issue.data, FAZENDO=form_alteracao.fazer.data,
                                     FAZER=form_alteracao.fazer.data, COMO=form_alteracao.como.data, VERSAO=form_alteracao.versao.data,
                                     DOCS=complete_name, ALT_CUST=form_alteracao.alt_cust.data, ANALISTA_ID=current_user.id)
            database.session.add(alteracao)
            database.session.commit()
            flash('Solicitação feita com sucesso', 'alert-success')
            return True


def solErro(form_erro):
    if form_erro.validate_on_submit() and 'btn_submit_inserir' in request.form:
        erro = SOL_ERRO.query.filter_by(
            NRO_TP=form_erro.nro_tp.data).first()

        if erro:
            flash(
                'Já existe solicitação de analise de erro para essa TP', 'alert-danger')
        else:
            name, extension = os.path.splitext(
                form_erro.docs.data.filename)
            name = str(form_erro.nro_tp.data) + '-' + \
                datetime.today().strftime('%d-%m-%Y.%H:%M')
            complete_name = name + extension
            complete_path = os.path.join(
                app.root_path, 'static', 'docs', 'erro', complete_name)
            form_erro.docs.data.save(complete_path)

            erro = SOL_ERRO(NRO_TP=form_erro.nro_tp.data, ISSUE=form_erro.issue.data, CAMINHO_MENU=form_erro.menu_dir.data, 
                            CODIGO_MENU=form_erro.menu_cod.data, FAZENDO=form_erro.fazer.data, FAZER=form_erro.fazer.data, 
                            PALIATIVA=form_erro.paliativa.data, DOCS=complete_name, BANCO=form_erro.db_teste.data, VERSAO=form_erro.versao.data, 
                            VERSAO_ANT=form_erro.versao_ant.data, ANALISTA_ID=current_user.id)
            database.session.add(erro)

            mov = MOV_SOL(NRO_TP=form_erro.nro_tp.data, TITULO='Abertura de Analise', TIPO='A', HELPER='', ANALISTA=current_user.USUARIO, RESUMO='Solicitação de erro aberta', STATUS='AGUARDANDO INICIALIZAÇÂO')
            database.session.add(mov)

            database.session.commit()
            flash('Solicitação feita com sucesso', 'alert-success')
            return True

def ajusteData(data):
    fuso_horario = datetime.timezone(timedelta(hours=-3))

    data = data.astimezone(fuso_horario)
    data = data.strftime('%d/%m/%Y %H:%M')

    return data
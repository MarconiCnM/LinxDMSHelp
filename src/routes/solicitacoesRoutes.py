from flask import Flask, redirect, render_template, url_for, request, send_from_directory
from flask_login import login_required, current_user
import os

from views.solicitacaoForms import FormAlteracao, FormErro
from controllers.solicitacaoController import solErro, solErroTime, formatDate, formatDateTime
from models.models import SOL_ERRO, MOV_SOL

def init_app(app: Flask):
    @app.route("/solicitacoes/alteracao", methods=['GET', 'POST'])
    @login_required
    def solicitacaoAlteracao():
        return render_template('main/solicitacoes/requisicao/alteracao.html')

    @app.route("/solicitacoes/compilacao", methods=['GET', 'POST'])
    @login_required
    def solicitacaoCompilacao():
        return render_template('main/solicitacoes/requisicao/compilacao.html')

    @app.route("/solerro", methods=['GET', 'POST'])
    @login_required
    def solicitacaoErro():
        erros = SOL_ERRO.query.filter_by(ANALISTA_ID=current_user.id)
        format_date = formatDate
        form_erro = FormErro()
        erro = solErro(form_erro)
        if erro:
            return redirect(url_for('dashboard'))
        return render_template('main/solicitacoes/requisicao/erro.html', form_erro=form_erro, erros=erros, format_date=format_date)
    
    @app.route("/solerro/requisicao/<erro_id>", methods=['GET', 'POST'])
    @login_required
    def solicitacaoErroID(erro_id):
        erroID = SOL_ERRO.query.get(erro_id)
        form_erro = FormErro()
        format_date_time = formatDateTime

        if erroID and request.method == 'GET':
            form_erro.nro_tp.data=erroID.NRO_TP
            form_erro.issue.data = erroID.ISSUE
            form_erro.menu_dir.data = erroID.CAMINHO_MENU
            form_erro.menu_cod.data = erroID.CODIGO_MENU
            form_erro.fazendo.data = erroID.FAZENDO
            form_erro.fazer.data = erroID.FAZER
            form_erro.paliativa.data = erroID.PALIATIVA
            form_erro.db_teste.data = erroID.BANCO
            form_erro.versao.data = erroID.VERSAO
            form_erro.versao_ant.data = erroID.VERSAO_ANT
            form_erro.solucao.data = erroID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=erroID.NRO_TP)
        erros = SOL_ERRO.query.all()
        erro = solErro(form_erro)
        if erro:
            return redirect(url_for('dashboard'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=erroID.NRO_TP)
        return render_template('main/solicitacoes/requisicao/erro.html', form_erro=form_erro, erros=erros, erroID=erroID, movs=movs, format_date_time=format_date_time)

    @app.route("/solerro/analise/", methods=['GET', 'POST'])
    @login_required
    def analiseErro():
        erros = solErroTime()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/helper/erro.html', erros=erros, format_date=format_date)
    
    @app.route("/solerro/analise/<erro_id>", methods=['GET', 'POST'])
    @login_required
    def analiseErroID(erro_id):
        erroID = SOL_ERRO.query.get(erro_id)
        form_erro = FormErro()
        format_date_time = formatDateTime
        if erroID and request.method == 'GET':
            form_erro.nro_tp.data=erroID.NRO_TP
            form_erro.issue.data = erroID.ISSUE
            form_erro.menu_dir.data = erroID.CAMINHO_MENU
            form_erro.menu_cod.data = erroID.CODIGO_MENU
            form_erro.fazendo.data = erroID.FAZENDO
            form_erro.fazer.data = erroID.FAZER
            form_erro.paliativa.data = erroID.PALIATIVA
            form_erro.db_teste.data = erroID.BANCO
            form_erro.versao.data = erroID.VERSAO
            form_erro.versao_ant.data = erroID.VERSAO_ANT
            form_erro.solucao.data = erroID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=erroID.NRO_TP)
        erros = SOL_ERRO.query.all()
        erro = solErro(form_erro)
        if erro:
            return redirect(url_for('analiseErro'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=erroID.NRO_TP)

        return render_template('main/solicitacoes/analise/erro.html', form_erro=form_erro, erros=erros, erroID=erroID, movs=movs, format_date_time=format_date_time)


    @app.route("/solicitacoes/help", methods=['GET', 'POST'])
    @login_required
    def solicitacaoHelp():
        return render_template('main/solicitacoes/requisicao/help.html')

    @app.route("/solicitacoes/importacao", methods=['GET', 'POST'])
    @login_required
    def solicitacaoImportacao():
        return render_template('main/solicitacoes/requisicao/importacao.html')

    @app.route("/solicitacoes/servico", methods=['GET', 'POST'])
    @login_required
    def solicitacaoServico():
        return render_template('main/solicitacoes/requisicao/servico.html')
    
    @app.route("/solicitacoes/share", methods=['GET', 'POST'])
    @login_required
    def solicitacaoShare():
        return render_template('main/solicitacoes/requisicao/share.html')

    @app.route("/errodoc/<erro_id>", methods=['GET', 'POST'])
    @login_required
    def errodoc(erro_id):
        erroID = SOL_ERRO.query.get(erro_id)

        name = erroID.DOCS

        dir_name = os.path.join(
                app.root_path, 'static', 'docs', 'erro')

        return send_from_directory(dir_name, name, as_attachment=True)
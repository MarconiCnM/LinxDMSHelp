from flask import Flask, redirect, render_template, url_for, request
from flask_login import login_required

from views.solicitacaoForms import FormAlteracao, FormErro
from controllers.solicitacaoController import ajusteData, solAlteracao, solErro
from models.models import SOL_ERRO, MOV_SOL

def init_app(app: Flask):
    @app.route("/solicitacoes/alteracao", methods=['GET', 'POST'])
    @login_required
    def solicitacaoAlteracao():
        form_alteracao = FormAlteracao()
        alterar = solAlteracao(form_alteracao)
        if alterar:
            return redirect(url_for('dashboard'))
        return render_template('main/solicitacoes/requisicao/alteracao.html', form_alteracao=form_alteracao)

    @app.route("/solicitacoes/compilacao", methods=['GET', 'POST'])
    @login_required
    def solicitacaoCompilacao():
        return render_template('main/solicitacoes/requisicao/compilacao.html')

    @app.route("/solicitacoes/erro", methods=['GET', 'POST'])
    @login_required
    def solicitacaoErro():
        erros = SOL_ERRO.query.all()
        form_erro = FormErro()
        erro = solErro(form_erro)
        if erro:
            return redirect(url_for('dashboard'))
        return render_template('main/solicitacoes/requisicao/erro.html', form_erro=form_erro, erros=erros)
    
    @app.route("/solicitacoes/erro/<erro_id>", methods=['GET', 'POST'])
    @login_required
    def solicitacaoErroID(erro_id):
        erroID = SOL_ERRO.query.get(erro_id)
        form_erro = FormErro()
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

            movs = MOV_SOL.query.filter_by(NRO_TP=erroID.NRO_TP)
            ajusteDta = ajusteData
        erros = SOL_ERRO.query.all()
        erro = solErro(form_erro)
        if erro:
            return redirect(url_for('dashboard'))
        return render_template('main/solicitacoes/requisicao/erro.html', form_erro=form_erro, erros=erros, erroID=erroID, movs=movs, ajusteDta=ajusteDta)


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
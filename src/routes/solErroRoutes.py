from flask import Flask, redirect, render_template, url_for, request, send_from_directory, flash
from flask_login import login_required, current_user
import os
from datetime import datetime

from views.solicitacaoForms import FormErro
from controllers.solErroController import solErro, solErroTime, formatDate, formatDateTime, solErroTimeGestor, solErroTimeCoordenador
from models.models import SOL_ERRO, MOV_SOL, GESTOR

def init_app(app: Flask):
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
    
    @app.route("/solerro/<erro_id>", methods=['GET', 'POST'])
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

    @app.route("/errodoc/<erro_id>", methods=['GET', 'POST'])
    @login_required
    def errodoc(erro_id):
        erroID = SOL_ERRO.query.get(erro_id)

        name = erroID.DOCS

        dir_name = os.path.join(
                app.root_path, 'static', 'docs', 'erro')

        return send_from_directory(dir_name, name, as_attachment=True)

    @app.route("/modissueerro/<erro_id>", methods=['GET', 'POST'])
    @login_required
    def modissueerro(erro_id):
        erroID = SOL_ERRO.query.get(erro_id)
        texto = f"""*Número da TP:* {erroID.NRO_TP}

*Caminho do Menu:* {erroID.CAMINHO_MENU}
*Código do Menu:* {erroID.CODIGO_MENU}

*O que o sistema está fazendo:* {erroID.FAZENDO}

*O que o sistema deveria fazer:* {erroID.FAZER}

*Paliativa:* {erroID.PALIATIVA}

*Banco de dados:* {erroID.BANCO}

*Versão:* {erroID.VERSAO}
*Ocorre na versão anterior:* {erroID.VERSAO_ANT}
        
        """

        name = 'Modelo_issue_erro-' + datetime.today().strftime('%d-%m-%Y') + '.txt'
        dir_name = os.path.join(
                app.root_path, 'static', 'exp\\')
  
        arquivo = open(dir_name + name, 'w') 
        arquivo.write(texto)
        arquivo.close()

        flash('Exportação realizada com sucesso', 'alert-sucess')

        return send_from_directory(dir_name, name, as_attachment=True)

    @app.route("/solerro/list/", methods=['GET', 'POST'])
    @login_required
    def listagemErro():
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                erros = solErroTimeCoordenador()
            else:
                erros = solErroTimeGestor()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/gestor/erro.html', erros=erros, format_date=format_date)
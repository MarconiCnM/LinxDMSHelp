from flask import Flask, redirect, render_template, url_for, request, send_from_directory, flash
from flask_login import login_required, current_user
import os
from datetime import datetime

from views.solicitacaoForms import FormAlteracao
from controllers.solAlteracaoController import solAlteracao, solAlteracaoTime, solAlteracaoTimeGestor, formatDate, formatDateTime, solAlteracaoTimeCoordenador
from models.models import SOL_HISTORIA, MOV_SOL, GESTOR

def init_app(app: Flask):
    @app.route("/solAlteracao", methods=['GET', 'POST'])
    @login_required
    def solicitacaoAlteracao():
        alteracoes = SOL_HISTORIA.query.filter_by(ANALISTA_ID=current_user.id)
        format_date = formatDate
        form_alteracao = FormAlteracao()
        alteracao = solAlteracao(form_alteracao)
        if alteracao:
            return redirect(url_for('dashboard'))
        return render_template('main/solicitacoes/requisicao/alteracao.html', form_alteracao=form_alteracao, alteracoes=alteracoes, format_date=format_date)
    
    @app.route("/solAlteracao/<alteracao_id>", methods=['GET', 'POST'])
    @login_required
    def solicitacaoAlteracaoID(alteracao_id):
        alteracaoID = SOL_HISTORIA.query.get(alteracao_id)
        form_alteracao = FormAlteracao()
        format_date_time = formatDateTime

        if alteracaoID and request.method == 'GET':
            form_alteracao.nro_tp.data=alteracaoID.NRO_TP
            form_alteracao.issue.data = alteracaoID.ISSUE
            form_alteracao.fazendo.data = alteracaoID.FAZENDO
            form_alteracao.fazer.data = alteracaoID.FAZER
            form_alteracao.como.data = alteracaoID.COMO
            form_alteracao.beneficio.data = alteracaoID.BENEFICIO
            form_alteracao.versao.data = alteracaoID.VERSAO
            form_alteracao.solucao.data = alteracaoID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=alteracaoID.NRO_TP)
        alteracoes = SOL_HISTORIA.query.all()
        alteracao = solAlteracao(form_alteracao)
        if alteracao:
            return redirect(url_for('dashboard'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=alteracaoID.NRO_TP)
        return render_template('main/solicitacoes/requisicao/alteracao.html', form_alteracao=form_alteracao, alteracoes=alteracoes, alteracaoID=alteracaoID, movs=movs, format_date_time=format_date_time)

    @app.route("/solAlteracao/analise/", methods=['GET', 'POST'])
    @login_required
    def analiseAlteracao():
        alteracoes = solAlteracaoTime()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/helper/alteracao.html', alteracoes=alteracoes, format_date=format_date)
    
    @app.route("/solAlteracao/analise/<alteracao_id>", methods=['GET', 'POST'])
    @login_required
    def analisealteracaoID(alteracao_id):
        alteracaoID = SOL_HISTORIA.query.get(alteracao_id)
        form_alteracao = FormAlteracao()
        format_date_time = formatDateTime
        if alteracaoID and request.method == 'GET':
            form_alteracao.nro_tp.data = alteracaoID.NRO_TP
            form_alteracao.issue.data = alteracaoID.ISSUE
            form_alteracao.fazendo.data = alteracaoID.FAZENDO
            form_alteracao.fazer.data = alteracaoID.FAZER
            form_alteracao.como.data = alteracaoID.COMO
            form_alteracao.beneficio.data = alteracaoID.BENEFICIO
            form_alteracao.versao.data = alteracaoID.VERSAO
            form_alteracao.solucao.data = alteracaoID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=alteracaoID.NRO_TP)
        alteracoes = SOL_HISTORIA.query.all()
        alteracao = solAlteracao(form_alteracao)
        if alteracao:
            return redirect(url_for('analiseAlteracao'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=alteracaoID.NRO_TP)

        return render_template('main/solicitacoes/analise/alteracao.html', form_alteracao=form_alteracao, alteracoes=alteracoes, alteracaoID=alteracaoID, movs=movs, format_date_time=format_date_time)

    @app.route("/alteracaodoc/<alteracao_id>", methods=['GET', 'POST'])
    @login_required
    def alteracaodoc(alteracao_id):
        alteracaoID = SOL_HISTORIA.query.get(alteracao_id)

        name = alteracaoID.DOCS

        dir_name = os.path.join(
                app.root_path, 'static', 'docs', 'alteracao')

        return send_from_directory(dir_name, name, as_attachment=True)


    @app.route("/modissuealt/<alt_id>", methods=['GET', 'POST'])
    @login_required
    def modissuealt(alt_id):
        alteracaoID = SOL_HISTORIA.query.get(alt_id)
        texto = f"""*Número da TP:* {alteracaoID.NRO_TP}

*O que o sistema está fazendo:* {alteracaoID.FAZENDO}

*O que o sistema deveria fazer:* {alteracaoID.FAZER}

*Como deseja que o sistema faça:* {alteracaoID.COMO}

*Qual o beneficio dessa alteração:* {alteracaoID.BENEFICIO}

*Versão:* {alteracaoID.VERSAO}
        
        """

        name = 'Modelo_issue_alt-' + datetime.today().strftime('%d-%m-%Y') + '.txt'
        dir_name = os.path.join(
                app.root_path, 'static', 'exp\\')
  
        arquivo = open(dir_name + name, 'w') 
        arquivo.write(texto)
        arquivo.close()

        flash('Exportação realizada com sucesso', 'alert-sucess')

        return send_from_directory(dir_name, name, as_attachment=True)

    @app.route("/solAlteracao/list/", methods=['GET', 'POST'])
    @login_required
    def listagemAlteracao():
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                alteracoes = solAlteracaoTimeCoordenador()
            else:
                alteracoes = solAlteracaoTimeGestor()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/gestor/alteracao.html', alteracoes=alteracoes, format_date=format_date)
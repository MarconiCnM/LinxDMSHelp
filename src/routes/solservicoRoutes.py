from flask import Flask, redirect, render_template, url_for, request, send_from_directory
from flask_login import login_required, current_user
import os

from views.solicitacaoForms import FormServico
from controllers.solServicoController import solServico, solServicoTime, formatDate, formatDateTime, solServicoTimeGestor, solServicoTimeCoordenador
from models.models import SOL_SERVICO, MOV_SOL, GESTOR

def init_app(app: Flask):
    @app.route("/solservico", methods=['GET', 'POST'])
    @login_required
    def solicitacaoServico():
        servicos = SOL_SERVICO.query.filter_by(ANALISTA_ID=current_user.id)
        format_date = formatDate
        form_servico = FormServico()
        servico = solServico(form_servico)
        if servico:
            return redirect(url_for('dashboard'))
        return render_template('main/solicitacoes/requisicao/servico.html', form_servico=form_servico, servicos=servicos, format_date=format_date)
    
    @app.route("/solservico/<servico_id>", methods=['GET', 'POST'])
    @login_required
    def solicitacaoservicoID(servico_id):
        servicoID = SOL_SERVICO.query.get(servico_id)
        form_servico = FormServico()
        format_date_time = formatDateTime

        if servicoID and request.method == 'GET':
            form_servico.nro_tp.data=servicoID.NRO_TP
            form_servico.franqueado.data = servicoID.FRANQUEADO
            form_servico.descricao.data = servicoID.DESC
            form_servico.analise.data = servicoID.ANALISE
            form_servico.solucao.data = servicoID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=servicoID.NRO_TP)
        servicos = SOL_SERVICO.query.all()
        servico = solServico(form_servico)
        if servico:
            return redirect(url_for('dashboard'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=servicoID.NRO_TP)
        return render_template('main/solicitacoes/requisicao/servico.html', form_servico=form_servico, servicos=servicos, servicoID=servicoID, movs=movs, format_date_time=format_date_time)

    @app.route("/solservico/analise/", methods=['GET', 'POST'])
    @login_required
    def analiseServico():
        servicos = solServicoTime()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/helper/servico.html', servicos=servicos, format_date=format_date)
    
    @app.route("/solservico/analise/<servico_id>", methods=['GET', 'POST'])
    @login_required
    def analiseServicoID(servico_id):
        servicoID = SOL_SERVICO.query.get(servico_id)
        form_servico = FormServico()
        format_date_time = formatDateTime
        if servicoID and request.method == 'GET':
            form_servico.nro_tp.data=servicoID.NRO_TP
            form_servico.franqueado.data = servicoID.FRANQUEADO
            form_servico.descricao.data = servicoID.DESC
            form_servico.analise.data = servicoID.ANALISE
            form_servico.solucao.data = servicoID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=servicoID.NRO_TP)
        servicos = SOL_SERVICO.query.all()
        servico = solServico(form_servico)
        if servico:
            return redirect(url_for('analiseServico'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=servicoID.NRO_TP)

        return render_template('main/solicitacoes/analise/servico.html', form_servico=form_servico, servicos=servicos, servicoID=servicoID, movs=movs, format_date_time=format_date_time)


    @app.route("/solservico/list/", methods=['GET', 'POST'])
    @login_required
    def listagemServico():
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                servicos = solServicoTimeCoordenador()
            else:
                servicos = solServicoTimeGestor()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/gestor/servico.html', servicos=servicos, format_date=format_date)
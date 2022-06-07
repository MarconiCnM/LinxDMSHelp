from flask import Flask, redirect, render_template, url_for, request, send_from_directory
from flask_login import login_required, current_user
import os

from views.solicitacaoForms import FormImport
from controllers.solImportController import solImport, solImportTime, formatDate, formatDateTime, solImportTimeGestor, solImportTimeCoordenador
from models.models import SOL_IMPORT, MOV_SOL, GESTOR

def init_app(app: Flask):
    @app.route("/solimp", methods=['GET', 'POST'])
    @login_required
    def solicitacaoImport():
        imps = SOL_IMPORT.query.filter_by(ANALISTA_ID=current_user.id)
        format_date = formatDate
        form_imp = FormImport()
        imp = solImport(form_imp)
        if imp:
            return redirect(url_for('dashboard'))
        return render_template('main/solicitacoes/requisicao/importacao.html', form_imp=form_imp, imps=imps, format_date=format_date)

    @app.route("/solimp/<imp_id>", methods=['GET', 'POST'])
    @login_required
    def solicitacaoImportID(imp_id):
        impID = SOL_IMPORT.query.get(imp_id)
        form_imp = FormImport()
        format_date_time = formatDateTime

        if impID and request.method == 'GET':
            form_imp.nro_tp.data=impID.NRO_TP
            form_imp.grupo.data = impID.GRUPO
            form_imp.issue.data = impID.ISSUE
            form_imp.schema.data = impID.SCHEMA
            form_imp.tamanho.data = impID.TAMANHO
            form_imp.servidor.data = impID.SERVIDOR
            form_imp.link.data = impID.DIR_ARQ
            form_imp.observacao.data = impID.OBS
            form_imp.solucao.data = impID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=impID.NRO_TP)
        imps = SOL_IMPORT.query.all()
        imp = solImport(form_imp)
        if imp:
            return redirect(url_for('dashboard'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=impID.NRO_TP)
        return render_template('main/solicitacoes/requisicao/importacao.html', form_imp=form_imp, imps=imps, impID=impID, movs=movs, format_date_time=format_date_time)

    @app.route("/solimp/analise/", methods=['GET', 'POST'])
    @login_required
    def analiseImport():
        imps = solImportTime()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/helper/importacao.html', imps=imps, format_date=format_date)
    
    @app.route("/solimp/analise/<imp_id>", methods=['GET', 'POST'])
    @login_required
    def analiseImportID(imp_id):
        impID = SOL_IMPORT.query.get(imp_id)
        form_imp = FormImport()
        format_date_time = formatDateTime
        if impID and request.method == 'GET':
            form_imp.nro_tp.data=impID.NRO_TP
            form_imp.grupo.data = impID.GRUPO
            form_imp.issue.data = impID.ISSUE
            form_imp.schema.data = impID.SCHEMA
            form_imp.tamanho.data = impID.TAMANHO
            form_imp.servidor.data = impID.SERVIDOR
            form_imp.link.data = impID.DIR_ARQ
            form_imp.observacao.data = impID.OBS
            form_imp.solucao.data = impID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=impID.NRO_TP)
        imps = SOL_IMPORT.query.all()
        imp = solImport(form_imp)
        if imp:
            return redirect(url_for('analiseImport'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=impID.NRO_TP)

        return render_template('main/solicitacoes/analise/importacao.html', form_imp=form_imp, imps=imps, impID=impID, movs=movs, format_date_time=format_date_time)

    @app.route("/solimp/list/", methods=['GET', 'POST'])
    @login_required
    def listagemImport():
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                imps = solImportTimeCoordenador()
            else:
                imps = solImportTimeGestor()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/gestor/importacao.html', imps=imps, format_date=format_date)
    
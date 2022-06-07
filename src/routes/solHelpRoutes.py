from flask import Flask, redirect, render_template, url_for, request, send_from_directory, flash
from flask_login import login_required, current_user
import os
from datetime import datetime

from views.solicitacaoForms import FormHelp
from controllers.solHelpController import solHelp, solHelpTime, formatDate, formatDateTime, solHelpTimeGestor, solHelpTimeCoordenador
from models.models import HELP, MOV_SOL, GESTOR

def init_app(app: Flask):
    @app.route("/solhelp", methods=['GET', 'POST'])
    @login_required
    def solicitacaoHelp():
        helps = HELP.query.filter_by(ANALISTA_ID=current_user.id)
        format_date = formatDate
        form_help = FormHelp()
        help = solHelp(form_help)
        if help:
            return redirect(url_for('dashboard'))
        return render_template('main/solicitacoes/requisicao/help.html', form_help=form_help, helps=helps, format_date=format_date)
    
    @app.route("/solhelp/<help_id>", methods=['GET', 'POST'])
    @login_required
    def solicitacaoHelpID(help_id):
        helpID = HELP.query.get(help_id)
        form_help = FormHelp()
        format_date_time = formatDateTime

        if helpID and request.method == 'GET':
            form_help.nro_tp.data=helpID.NRO_TP
            form_help.menu_dir.data = helpID.CAMINHO_MENU
            form_help.menu_cod.data = helpID.CODIGO_MENU
            form_help.problema.data = helpID.PROBLEMA
            form_help.analisado.data = helpID.ANALISADO
            form_help.duvida.data = helpID.DUVIDA
            form_help.paliativa.data = helpID.PALIATIVA
            form_help.db_teste.data = helpID.BANCO
            form_help.versao.data = helpID.VERSAO
            form_help.solucao.data = helpID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=helpID.NRO_TP)
        helps = HELP.query.all()
        help = solHelp(form_help)
        if help:
            return redirect(url_for('dashboard'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=helpID.NRO_TP)
        return render_template('main/solicitacoes/requisicao/help.html', form_help=form_help, helps=helps, helpID=helpID, movs=movs, format_date_time=format_date_time)

    @app.route("/solhelp/analise/", methods=['GET', 'POST'])
    @login_required
    def analiseHelp():
        helps = solHelpTime()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/helper/help.html', helps=helps, format_date=format_date)
    
    @app.route("/solhelp/analise/<help_id>", methods=['GET', 'POST'])
    @login_required
    def analiseHelpID(help_id):
        helpID = HELP.query.get(help_id)
        form_help = FormHelp()
        format_date_time = formatDateTime
        if helpID and request.method == 'GET':
            form_help.nro_tp.data=helpID.NRO_TP
            form_help.menu_dir.data = helpID.CAMINHO_MENU
            form_help.menu_cod.data = helpID.CODIGO_MENU
            form_help.problema.data = helpID.PROBLEMA
            form_help.analisado.data = helpID.ANALISADO
            form_help.duvida.data = helpID.DUVIDA
            form_help.paliativa.data = helpID.PALIATIVA
            form_help.db_teste.data = helpID.BANCO
            form_help.versao.data = helpID.VERSAO
            form_help.solucao.data = helpID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=helpID.NRO_TP)
        helps = HELP.query.all()
        help = solHelp(form_help)
        if help:
            return redirect(url_for('analiseHelp'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=helpID.NRO_TP)

        return render_template('main/solicitacoes/analise/help.html', form_help=form_help, helps=helps, helpID=helpID, movs=movs, format_date_time=format_date_time)


    @app.route("/helpdoc/<help_id>", methods=['GET', 'POST'])
    @login_required
    def helpdoc(help_id):
        helpID = HELP.query.get(help_id)

        name = helpID.DOCS

        dir_name = os.path.join(
                app.root_path, 'static', 'docs', 'help')

        return send_from_directory(dir_name, name, as_attachment=True)

    @app.route("/solhelp/list/", methods=['GET', 'POST'])
    @login_required
    def listagemHelp():
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                helps = solHelpTimeCoordenador()
            else:
                helps = solHelpTimeGestor()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/gestor/help.html', helps=helps, format_date=format_date)
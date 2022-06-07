from flask import Flask, redirect, render_template, url_for, request, send_from_directory
from flask_login import login_required, current_user
import os

from views.solicitacaoForms import FormShare
from controllers.solShareController import solShare, solShareTime, formatDate, formatDateTime, solShareTimeGestor, solShareTimeCoordenador
from models.models import SOL_SHARE, MOV_SOL, GESTOR

def init_app(app: Flask):
    @app.route("/solshare", methods=['GET', 'POST'])
    @login_required
    def solicitacaoShare():
        shares = SOL_SHARE.query.filter_by(ANALISTA_ID=current_user.id)
        format_date = formatDate
        form_share = FormShare()
        share = solShare(form_share)
        if share:
            return redirect(url_for('dashboard'))
        return render_template('main/solicitacoes/requisicao/share.html', form_share=form_share, shares=shares, format_date=format_date)

    @app.route("/solshare/<share_id>", methods=['GET', 'POST'])
    @login_required
    def solicitacaoShareID(share_id):
        shareID = SOL_SHARE.query.get(share_id)
        form_share = FormShare()
        format_date_time = formatDateTime

        if shareID and request.method == 'GET':
            form_share.titulo.data=shareID.TITULO
            form_share.produto.data = shareID.PRODUTO
            form_share.modulo.data = shareID.MODULO
            form_share.finalidade.data = shareID.FINALIDADE
            form_share.link.data = shareID.LINK
            form_share.solucao.data = shareID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=shareID.id)
        shares = SOL_SHARE.query.all()
        share = solShare(form_share)
        if share:
            return redirect(url_for('dashboard'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=shareID.id)
        return render_template('main/solicitacoes/requisicao/share.html', form_share=form_share, shares=shares, shareID=shareID, movs=movs, format_date_time=format_date_time)

    @app.route("/solshare/analise/", methods=['GET', 'POST'])
    @login_required
    def analiseShare():
        shares = solShareTime()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/helper/share.html', shares=shares, format_date=format_date)
    
    @app.route("/solshare/analise/<share_id>", methods=['GET', 'POST'])
    @login_required
    def analiseShareID(share_id):
        shareID = SOL_SHARE.query.get(share_id)
        form_share = FormShare()
        format_date_time = formatDateTime
        if shareID and request.method == 'GET':
            form_share.titulo.data=shareID.TITULO
            form_share.produto.data = shareID.PRODUTO
            form_share.modulo.data = shareID.MODULO
            form_share.finalidade.data = shareID.FINALIDADE
            form_share.link.data = shareID.LINK
            form_share.solucao.data = shareID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=shareID.id)
        shares = SOL_SHARE.query.all()
        share = solShare(form_share)
        if share:
            return redirect(url_for('analiseShare'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=shareID.id)

        return render_template('main/solicitacoes/analise/share.html', form_share=form_share, shares=shares, shareID=shareID, movs=movs, format_date_time=format_date_time)

    @app.route("/solshare/list/", methods=['GET', 'POST'])
    @login_required
    def listagemShare():
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                shares = solShareTimeCoordenador()
            else: 
                shares = solShareTimeGestor()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/gestor/share.html', shares=shares, format_date=format_date)
    
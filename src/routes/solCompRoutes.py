from flask import Flask, redirect, render_template, url_for, request, send_from_directory, flash
from flask_login import login_required, current_user
import os
from datetime import datetime

from views.solicitacaoForms import FormComp
from controllers.solCompController import solComp, solCompTime, formatDate, formatDateTime, solCompTimeGestor, solCompTimeCoordenador
from models.models import SOL_SCRIPT, MOV_SOL, GESTOR

def init_app(app: Flask):
    @app.route("/solcomp", methods=['GET', 'POST'])
    @login_required
    def solicitacaoComp():
        comps = SOL_SCRIPT.query.filter_by(ANALISTA_ID=current_user.id)
        format_date = formatDate
        form_comp = FormComp()
        comp = solComp(form_comp)
        if comp:
            return redirect(url_for('dashboard'))
        return render_template('main/solicitacoes/requisicao/compilacao.html', form_comp=form_comp, comps=comps, format_date=format_date)
    
    @app.route("/solcomp/<comp_id>", methods=['GET', 'POST'])
    @login_required
    def solicitacaoCompID(comp_id):
        compID = SOL_SCRIPT.query.get(comp_id)
        form_comp = FormComp()
        format_date_time = formatDateTime

        if compID and request.method == 'GET':
            form_comp.nro_tp.data=compID.NRO_TP
            form_comp.grupo.data = compID.GRUPO
            form_comp.oque.data = compID.OQUE
            form_comp.porque.data = compID.PORQUE
            form_comp.solucao.data = compID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=compID.NRO_TP)
        comps = SOL_SCRIPT.query.all()
        comp = solComp(form_comp)
        if comp:
            return redirect(url_for('dashboard'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=compID.NRO_TP)
        return render_template('main/solicitacoes/requisicao/compilacao.html', form_comp=form_comp, comps=comps, compID=compID, movs=movs, format_date_time=format_date_time)

    @app.route("/solcomp/analise/", methods=['GET', 'POST'])
    @login_required
    def analiseComp():
        comps = solCompTime()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/helper/compilacao.html', comps=comps, format_date=format_date)
    
    @app.route("/solcomp/analise/<comp_id>", methods=['GET', 'POST'])
    @login_required
    def analiseCompID(comp_id):
        compID = SOL_SCRIPT.query.get(comp_id)
        form_comp = FormComp()
        format_date_time = formatDateTime
        if compID and request.method == 'GET':
            form_comp.nro_tp.data=compID.NRO_TP
            form_comp.issue.data = compID.ISSUE
            form_comp.grupo.data = compID.GRUPO
            form_comp.oque.data = compID.OQUE
            form_comp.porque.data = compID.PORQUE
            form_comp.solucao.data = compID.SOLUCAO

            movs = MOV_SOL.query.filter_by(NRO_TP=compID.NRO_TP)
        comps = SOL_SCRIPT.query.all()
        comp = solComp(form_comp)
        if comp:
            return redirect(url_for('analiseComp'))
        else:
            movs = MOV_SOL.query.filter_by(NRO_TP=compID.NRO_TP)

        return render_template('main/solicitacoes/analise/compilacao.html', form_comp=form_comp, comps=comps, compID=compID, movs=movs, format_date_time=format_date_time)

    @app.route("/compscript/<comp_id>", methods=['GET', 'POST'])
    @login_required
    def compscript(comp_id):
        compID = SOL_SCRIPT.query.get(comp_id)

        name = compID.SCRIPT

        dir_name = os.path.join(
                app.root_path, 'static', 'docs', 'script')

        return send_from_directory(dir_name, name, as_attachment=True)

    @app.route("/modissuecomp/<comp_id>", methods=['GET', 'POST'])
    @login_required
    def modissuecomp(comp_id):
        compID = SOL_SCRIPT.query.get(comp_id)
        texto = f"""*Número da TP:* {compID.NRO_TP}

*Grupo* {compID.GRUPO}

*O que o script faz:* {compID.OQUE}

*Qual o motivo de não conseguirmos fazer pelo sistema:* {compID.PORQUE}

        """

        name = 'Modelo_issue_comp-' + datetime.today().strftime('%d-%m-%Y') + '.txt'
        dir_name = os.path.join(
                app.root_path, 'static', 'exp\\')
  
        arquivo = open(dir_name + name, 'w') 
        arquivo.write(texto)
        arquivo.close()

        flash('Exportação realizada com sucesso', 'alert-sucess')

        return send_from_directory(dir_name, name, as_attachment=True)

    @app.route("/solcomp/list/", methods=['GET', 'POST'])
    @login_required
    def listagemComp():
        if GESTOR.query.filter_by(EMAIL=current_user.EMAIL).first():
            if (current_user.EMAIL == 'admin@linx.com.br') or (current_user.EMAIL == 'rodrigo.silva@linx.com.br'):
                comps = solCompTimeCoordenador()
            else:
                comps = solCompTimeGestor()
        format_date = formatDate
        return render_template('main/solicitacoes/listagem/gestor/compilacao.html', comps=comps, format_date=format_date)
    
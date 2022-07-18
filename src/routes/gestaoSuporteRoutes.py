from click import command
from flask import Flask, redirect, render_template, url_for, request, send_from_directory, flash
from flask_login import login_required, current_user
from app import database
from datetime import datetime
from controllers.dashboardController import formatDate
import pandas as pd
import os

def init_app(app: Flask):
    @app.route("/consultaatendimento", methods=['GET', 'POST'])
    @login_required
    def consultaAtendimento():
        return render_template('main/gestaosuporte/consultaatendimento.html')
    
    @app.route("/consultachamados", methods=['GET', 'POST'])
    @login_required
    def consultaChamados():
        produtos = enumerate(database.session.execute('select distinct PRODUTO from CHAMADO_NEW where produto is not null').fetchall(), start=0)
        equipes = enumerate(database.session.execute('select NOME from time').fetchall(), start=0)
        analistas = enumerate(database.session.execute('select USUARIO from analista').fetchall(), start=0)
        helpers = enumerate(database.session.execute('select USUARIO from helper').fetchall(), start=0)
        clientes = enumerate(database.session.execute("select distinct no_conta from chamado_new where no_conta like 'GRUPO%'").fetchall(), start=0)
        status = enumerate(database.session.execute('select distinct no_status_tarefa from chamado_new').fetchall(), start=0)
        tipos = enumerate(database.session.execute('select distinct tipo_solicitacao from chamado_new where tipo_solicitacao is not null').fetchall(), start=0)
        
        if request.method == "POST":
            startdataAberto = request.form['startDateAberto']
            enddataAberto = request.form['endDateAberto']
            produtosEnd = request.form['listProduto']
            equipeEnd = request.form['listEquipe']
            analistasEnd = request.form['listAnalista']
            helpersEnd = request.form['listHelper']
            startdataEncerra = request.form['startDateEncerra']
            enddataEncerra = request.form['endDateEncerra']
            clientesEnd = request.form['listCliente']
            statusEnd = request.form['listStatus']
            tiposEnd = request.form['listTipo']
            npsvalor = request.form['npsvalor']
            afvalue = request.form['afvalue']
            fcrvalue = request.form['fcrvalue']
            reaberturavalue = request.form['reaberturavalue']
            slavalue = request.form['slavalue']

            comand = """SELECT * FROM [dbo].[CHAMADO_NEW] where id_tarefa is not null """

            if startdataAberto != '':
                if enddataAberto != '':
                    add = f" and DH_ABERTURA BETWEEN '{startdataAberto}' and '{enddataAberto}' "
                    comand += add
                else:
                    add = f" and DH_ABERTURA BETWEEN '{startdataAberto}' and '{datetime.today().strftime('%Y-%m-%d')}' "
                    comand += add
            
            if produtosEnd != '':
                add = f" and PRODUTO IN ({produtosEnd})"
                comand += add

            if equipeEnd != '':
                lista_analista = ""
                analista = database.session.execute("SELECT id, USUARIO " + 
                "FROM ANALISTA " + 
                F"WHERE TIME_ID in (SELECT ID FROM TIME WHERE nome in ({equipeEnd})) ").fetchall()
                for i in analista:
                    lsanalista = i[1].replace(' ', '.')
                    lista_analista += "'" + lsanalista.upper() + "',"
                
                add = f" and NO_RESPONSAVEL IN ({lista_analista[:-1]})"
                comand += add

            if analistasEnd != '':
                analistafim = analistasEnd.replace(' ', '.')
                add = f" and NO_RESPONSAVEL IN ({analistafim.upper()})"
                comand += add
            
            if helpersEnd != '':
                lista_analista = ""
                analista = database.session.execute("SELECT id, USUARIO " + 
                    "FROM ANALISTA " + 
                    F"WHERE TIME_ID in (SELECT id FROM TIME WHERE HELPER_ID in (select id from helper where usuario in ({helpersEnd}))) ").fetchall()
                for i in analista:
                    lsanalista = i[1].replace(' ', '.')
                    lista_analista += "'" + lsanalista.upper() + "',"
                add = f" and NO_RESPONSAVEL IN ({lista_analista[:-1]})"
                comand += add

            if startdataEncerra != '':
                if enddataEncerra != '':
                    add = f" and DH_CONCLUSAO BETWEEN '{startdataEncerra}' and '{enddataEncerra}' "
                    comand += add
                else:
                    add = f" and DH_CONCLUSAO BETWEEN '{startdataEncerra}' and '{datetime.today().strftime('%Y-%m-%d')}' "
                    comand += add
                
            if clientesEnd != '':
                add = f" and NO_CONTA IN ({clientesEnd})"
                comand += add

            if statusEnd != '':
                add = f" and NO_STATUS_TAREFA IN ({statusEnd})"
                comand += add

            if tiposEnd != '':
                add = f" and TIPO_SOLICITACAO IN ({tiposEnd})"
                comand += add

            if npsvalor != 'Todos':
                add = f" and NIVEL_NPS = {npsvalor.upper()}"
                comand += add

            if afvalue == 'Aberto':
                add = f" and DH_CONCLUSAO is null"
                comand += add
            elif afvalue == 'Encerrado':
                add = f" and DH_CONCLUSAO is not null"
                comand += add
        
            if fcrvalue != 'Ambos':
                add = f" and FCR = {fcrvalue.upper()}"
                comand += add
            
            if reaberturavalue == 'Sim':
                add = f" and NU_REABERTURA > 0"
                comand += add
            elif reaberturavalue == 'Não':
                add = f" and NU_REABERTURA = 0"
                comand += add
            
            if slavalue == "No SLA":
                add = f" and NO_SLA = 'No_SLA'"
                comand += add
            elif slavalue == 'Backlog':
                add = f" and NO_SLA = 'Backlog'"
                comand += add

            result =  enumerate(database.session.execute(comand).fetchall(), start=1)
            total = database.session.execute(comand.replace('SELECT * FROM [dbo].[CHAMADO_NEW]', 'SELECT count(*) FROM [dbo].[CHAMADO_NEW]')).fetchall()[0][0]
            format_date = formatDate
            carrega_resultado = 'S'
            
            return render_template('main/gestaosuporte/consultachamados.html', result=result, format_date=format_date, carrega_resultado=carrega_resultado, total=total, produtos=produtos, equipes=equipes, analistas=analistas, helpers=helpers, clientes=clientes, status=status, tipos=tipos)

        return render_template('main/gestaosuporte/consultachamados.html', produtos=produtos, equipes=equipes, analistas=analistas, helpers=helpers, clientes=clientes, status=status, tipos=tipos)

   
    @app.route("/relatorioatendimento", methods=['GET', 'POST'])
    @login_required
    def relatorioAtendimento():
        return render_template('main/gestaosuporte/relatorioatendimento.html')
    
    @app.route("/performancecolaborador", methods=['GET', 'POST'])
    @login_required
    def performanceColaborador():
        return render_template('main/gestaosuporte/performancecolaborador.html')
    
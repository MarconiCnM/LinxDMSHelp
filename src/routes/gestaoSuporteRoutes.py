from flask import Flask, redirect, render_template, url_for, request, send_from_directory, flash
from flask_login import login_required, current_user
from app import database
from datetime import datetime

def init_app(app: Flask):
    @app.route("/consultaatendimento", methods=['GET', 'POST'])
    @login_required
    def consultaAtendimento():
        return render_template('main/gestaosuporte/consultaatendimento.html')
    
    @app.route("/consultachamados", methods=['GET', 'POST'])
    @login_required
    def consultaChamados():
        produtos = database.session.execute('select distinct PRODUTO from CHAMADO_NEW where produto is not null').fetchall()
        equipes = database.session.execute('select NOME from time').fetchall()
        analistas = database.session.execute('select USUARIO from analista').fetchall()
        helpers = database.session.execute('select USUARIO from helper').fetchall()
        clientes = database.session.execute('select distinct no_conta from chamado_new').fetchall()
        status = database.session.execute('select distinct no_status_tarefa from chamado_new').fetchall()
        tipos = database.session.execute('select distinct tipo_solicitacao from chamado_new where tipo_solicitacao is not null').fetchall()
        return render_template('main/gestaosuporte/consultachamados.html', produtos=produtos, equipes=equipes, analistas=analistas, helpers=helpers, clientes=clientes, status=status, tipos=tipos)

    @app.route("/relatorioatendimento", methods=['GET', 'POST'])
    @login_required
    def relatorioAtendimento():
        return render_template('main/gestaosuporte/relatorioatendimento.html')
    
    @app.route("/performancecolaborador", methods=['GET', 'POST'])
    @login_required
    def performanceColaborador():
        return render_template('main/gestaosuporte/performancecolaborador.html')
    